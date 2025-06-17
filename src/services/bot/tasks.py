import logging

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from contents.models import PostType
from utils.bot import get_content_post, get_bot


async def send_post() -> None:
    """Отправляет пост в канал."""
    bot = get_bot()
    now = timezone.now()
    async for post_type in PostType.objects.filter(
        Q(time_publication__isnull=True) | Q(time_publication__hour=now.hour, time_publication__minute=now.minute),
        is_publish=True,
        posts__is_published=False,
    ):
        audios, images_videos, text, post = await get_content_post(
            is_published=False,
            types=post_type,
            datetime_publication__lte=now,
        )
        try:
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
        except Exception as e:
            logging.error(e)
