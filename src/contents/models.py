import os

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

from constants.models import (
    MAX_LEN_TITLE,
    UPLOAD_TO_CONTENT,
    IMAGE_FORMATS,
    VIDEO_FORMATS,
    AUDIO_FORMATS,
    MESSAGE_INCORRECT_FILE_FORMAT,
)


class Post(models.Model):
    """Модель поста."""

    title = models.CharField(
        max_length=MAX_LEN_TITLE,
        unique=True,
        verbose_name=_('Тайтл поста'),
        help_text=_('Тайтл поста'),
        db_comment=_('Тайтл поста'),
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Флаг опубликованности'),
        help_text=_('Флаг опубликованности'),
        db_comment=_('Флаг опубликованности'),
    )
    text = RichTextField(
        blank=True,
        null=True,
        verbose_name=_('Текст поста'),
        help_text=_('Текст поста'),
        db_comment=_('Текст поста'),
    )

    def __str__(self) -> str:
        return f'{self.pk}-{self.title}-{self.is_published}'

    class Meta:
        verbose_name = _('Пост')
        verbose_name_plural = _('Посты')


class MediaContent(models.Model):
    """Модель media-контета поста."""

    class Type(models.TextChoices):
        """Mapping типов контента."""

        IMAGE = 'image', _('Изображение')
        VIDEO = 'video', _('Видео')
        AUDIO = 'audio', _('Аудио')

    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='media_contents',
        verbose_name=_('Пост'),
        help_text=_('Пост'),
    )
    content = models.FileField(
        verbose_name=_('Контент'),
        help_text=_('Контент'),
        upload_to=UPLOAD_TO_CONTENT,
    )
    type = models.CharField(
        verbose_name=_('Тип контента'),
        help_text=_('Тип контента'),
        choices=Type.choices,
        default=Type.IMAGE,
    )

    def __str__(self) -> str:
        return f'{self.post}-{self.content}-{self.type}'

    class Meta:
        verbose_name = _('Media-контент поста')
        verbose_name_plural = _('Media-контент постов')

    def clean(self) -> None:
        """Валидация формата файла."""
        format = os.path.splitext(self.content.name)[1].replace('.', '').lower()
        if self.type == MediaContent.Type.IMAGE:
            if format not in IMAGE_FORMATS:
                raise ValidationError(MESSAGE_INCORRECT_FILE_FORMAT.format(format, ', '.join(IMAGE_FORMATS)))
        elif self.type == MediaContent.Type.VIDEO:
            if format not in VIDEO_FORMATS:
                raise ValidationError(MESSAGE_INCORRECT_FILE_FORMAT.format(format, ', '.join(VIDEO_FORMATS)))
        elif self.type == MediaContent.Type.AUDIO:
            if format not in AUDIO_FORMATS:
                raise ValidationError(MESSAGE_INCORRECT_FILE_FORMAT.format(format, ', '.join(AUDIO_FORMATS)))
