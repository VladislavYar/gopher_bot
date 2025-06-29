from datetime import datetime
import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.text_decorations import markdown_decoration
from aiogram.enums import InputMediaType, ParseMode
from aiogram.types.input_file import FSInputFile
from aiogram.types import InputMediaVideo, InputMediaPhoto, Message
from django.conf import settings
from django.db.models import Model
from django.utils import timezone
from html_to_markdown import convert_to_markdown

from contents.models import Post, MediaContent


async def get_content_post(
    **kwargs: bool | str | int | datetime | Model,
) -> tuple[
    list[FSInputFile],
    list[InputMediaPhoto | InputMediaVideo],
    str | None,
    Post | None,
]:
    """Отдаёт контент по посту в формате telegram-a.

    Args:
        kwargs (dict[str, bool, str, int, datetime]): данные для фильтрации.

    Returns:
        tuple[
            list[FSInputFile],
            list[InputMediaPhoto | InputMediaVideo],
            str | None, Post | None
            ]: кортеж списка аудио, медиа, текста и поста.
    """
    post: Post | None = (
        await Post.objects.filter(**kwargs)
        .extra(select={'random_id': 'random()'})
        .prefetch_related(
            'media_contents',
        )
        .order_by('random_id')
        .afirst()
    )
    if not post:
        return [], [], None, None

    audios = []
    images_videos = []
    text = markdown_decoration.quote(convert_to_markdown(post.text)) if post.text else None
    is_add_caption = True
    for media_content in post.media_contents.all():
        file = FSInputFile(media_content.content.path)
        data = {'caption': text} if is_add_caption else {}
        if media_content.type == MediaContent.Type.IMAGE:
            images_videos.append(InputMediaPhoto(type=InputMediaType.PHOTO, media=file, **data))
            is_add_caption = False
        if media_content.type == MediaContent.Type.VIDEO:
            images_videos.append(InputMediaVideo(type=InputMediaType.VIDEO, media=file, **data))
            is_add_caption = False
        elif media_content.type == MediaContent.Type.AUDIO:
            audios.append(file)

    return audios, images_videos, text, post


async def content_reply_to_message(
    message: Message,
    audios: list[FSInputFile],
    images_videos: list[InputMediaPhoto | InputMediaVideo],
    text: str | None,
) -> None:
    """Отправка контента в виде ответа на сообщение.

    Args:
        message (Message): сообщение.
        audios (list[FSInputFile]): файлы с аудио.
        images_videos (list[InputMediaPhoto  |  InputMediaVideo]): файлы с фото/видео.
        text (str | None): текст.
    """
    if not audios and not images_videos and text:
        await message.reply(text)
    if audios:
        for audio in audios:
            await message.reply_audio(audio, caption=text)
    if images_videos:
        await message.reply_media_group(images_videos)


def get_bot() -> Bot:
    """Отдаёт объект telegram-бота.

    Returns:
        Bot: telegram-бот.
    """
    return Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
    )


async def check_is_admin(message: Message) -> bool:
    """Проверка на админа.

    Args:
        message (Message): сообщение.

    Returns:
        bool: флаг проверка на админа.
    """
    bot = message.bot
    if bot is None:
        return False
    admins = await bot.get_chat_administrators(message.chat.id)
    user = message.from_user
    if not user:
        return False
    return any(admin.user.id == user.id for admin in admins)


def get_command(message: Message) -> str | None:
    """Отдаёт команду сообщения.

    Args:
        message (Message): сообщение.

    Returns:
        str | None: команда сообщения.
    """
    text = message.text
    if text and text.startswith('/') and len(text) > 1:
        if command := text[1:].split()[0]:
            return command


async def send_post_by_command(message: Message) -> None:
    """Отправка поста по команде.

    Args:
        message (Message): сообщение.
    """
    command = get_command(message)
    if not command:
        return
    filters = {} if await check_is_admin(message) else {'types__is_publish_by_admin': False}
    audios, images_videos, text, _ = await get_content_post(
        is_published=False,
        types__key=command,
        types__is_publish_by_command=True,
        datetime_publication__lte=timezone.now(),
        **filters,
    )
    try:
        if reply_to_message := message.reply_to_message:
            await content_reply_to_message(reply_to_message, audios, images_videos, text)
        else:
            await content_reply_to_message(message, audios, images_videos, text)
    except Exception as e:
        logging.error(e)
    await message.delete()
