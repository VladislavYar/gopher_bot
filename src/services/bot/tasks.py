from aiogram import Bot
from aiogram.types.input_file import FSInputFile
from aiogram.types import InputMediaVideo, InputMediaPhoto
from aiogram.enums import InputMediaType
from django.conf import settings
from html_to_markdown import convert_to_markdown

from contents.models import Post, MediaContent


async def send_post(bot: Bot) -> None:
    """Отправляет сообщение в канал.

    Args:
        bot (Bot): экземпляр бота.
    """
    post: Post | None = (
        await Post.objects.filter(
            is_published=False,
        )
        .extra(select={'random_id': 'random()'})
        .prefetch_related(
            'media_contents',
        )
        .order_by('random_id')
        .afirst()
    )
    if not post:
        return

    audios = []
    images_videos = []
    text = convert_to_markdown(post.text) if post.text else None
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

    if not audios and not images_videos and text:
        await bot.send_message(settings.BOT_CHANNEL, text)
    if audios:
        for audio in audios:
            await bot.send_audio(settings.BOT_CHANNEL, audio, caption=text)
    if images_videos:
        await bot.send_media_group(settings.BOT_CHANNEL, images_videos)

    post.is_published = True
    await post.asave()
