from aiogram import Bot
from django.conf import settings
from django.utils import timezone

from utils.bot import get_content_post


async def send_post(bot: Bot, type: str) -> None:
    """Отправляет пост в канал.

    Args:
        bot (Bot): экземпляр бота.
        type (str): тип поста.
    """
    audios, images_videos, text, post = await get_content_post(
        is_published=False,
        type=type,
        datetime_publication__lte=timezone.now(),
    )

    if not audios and not images_videos and text:
        await bot.send_message(settings.BOT_CHANNEL, text)
    if audios:
        for audio in audios:
            await bot.send_audio(settings.BOT_CHANNEL, audio, caption=text)
    if images_videos:
        await bot.send_media_group(settings.BOT_CHANNEL, images_videos)

    if post:
        post.is_published = True
        await post.asave()
