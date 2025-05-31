from datetime import datetime

from aiogram.enums import InputMediaType
from aiogram.types.input_file import FSInputFile
from aiogram.types import InputMediaVideo, InputMediaPhoto
from html_to_markdown import convert_to_markdown

from contents.models import Post, MediaContent


async def get_content_post(
    **kwargs: bool | str | int | datetime,
) -> tuple[
    list[FSInputFile],
    list[InputMediaPhoto | InputMediaVideo],
    str | None,
    Post | None,
]:
    """Отдаёт контент по посту в формате telegram-a.

    Args:
        kwargs (dict[str, bool, str, int, datetime]): данные для фильтрации.
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

    return audios, images_videos, text, post
