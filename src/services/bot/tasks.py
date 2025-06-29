import logging

from django.db.models import Q
from django.utils import timezone

from contents.models import PostType
from utils.bot import get_content_post, get_bot, send_post_by_channel as send_post


async def send_post_by_channel() -> None:
    """Отправляет пост в канал."""
    bot = get_bot()
    now = timezone.now()
    async for post_type in PostType.objects.filter(
        Q(time_publication__isnull=True) | Q(time_publication__hour=now.hour, time_publication__minute=now.minute),
        is_publish_by_cron=True,
        posts__is_published=False,
    ):
        audios, images_videos, text, post = await get_content_post(
            is_published=False,
            types=post_type,
            datetime_publication__lte=now,
        )
        try:
            await send_post(bot, audios, images_videos, text)
            if post:
                post.is_published = True
                await post.asave()
        except Exception as e:
            logging.error(e)
