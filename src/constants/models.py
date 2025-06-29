from enum import StrEnum

from django.utils.translation import gettext_lazy as _


MAX_LEN_TITLE = 255
UPLOAD_TO_CONTENT = 'contents/'
IMAGE_FORMATS = (
    'jpg',
    'jpeg',
    'png',
    'gif',
    'webp',
    'bmp',
    'svg',
)
VIDEO_FORMATS = (
    'mp4',
    'mov',
    'mkv',
    'avi',
)
AUDIO_FORMATS = (
    'mp3',
    'aac',
    'wav',
    'ogg',
    'flac',
)
MESSAGE_INCORRECT_FILE_FORMAT = _('Некорректный формат файла, текущий формат: {}. Доступные форматы: {}.')


class PostTypeEnum(StrEnum):
    """Enum базовых типов поста."""

    HAPPY = 'happy'
    SAD = 'sad'
    POST = 'post'
