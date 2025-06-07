import os

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
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
    datetime_publication = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Дата и время публикации'),
        help_text=_('Дата и время публикации'),
        db_comment=_('Дата и время публикации'),
    )

    def __str__(self) -> str:
        return f'{self.pk}-{self.title}-{self.is_published}'

    class Meta:
        verbose_name = _('Пост')
        verbose_name_plural = _('Посты')


class PostType(models.Model):
    """Модель типа поста."""

    title = models.CharField(
        max_length=MAX_LEN_TITLE,
        unique=True,
        verbose_name=_('Тайтл типа поста'),
        help_text=_('Тайтл типа поста'),
        db_comment=_('Тайтл типа поста'),
    )
    key = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name=_('Ключ типа поста'),
        help_text=_('Ключ типа поста'),
        db_comment=_('Ключ типа поста'),
    )
    time_publication = models.TimeField(
        blank=True,
        null=True,
        verbose_name=_('Время публикации'),
        help_text=_('Время публикации(если пустой, публикуется при кажом запуске cron)'),
        db_comment=_('Время публикации'),
    )
    is_publish = models.BooleanField(
        default=True,
        verbose_name=_('Флаг разрешения публикации'),
        help_text=_('Флаг разрешения публикации'),
        db_comment=_('Флаг разрешения публикации'),
    )
    posts = models.ManyToManyField(
        to=Post,
        blank=True,
        related_name='types',
        verbose_name=_('Посты типа постов'),
        help_text=_('Посты типа постов'),
    )

    def __str__(self) -> str:
        return f'{self.pk}-{self.title}-{self.key}'

    class Meta:
        verbose_name = _('Тип поста')
        verbose_name_plural = _('Тип поста')


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
        upload_to=UPLOAD_TO_CONTENT,
        verbose_name=_('Контент'),
        help_text=_('Контент'),
    )
    type = models.CharField(
        choices=Type.choices,
        default=Type.IMAGE,
        verbose_name=_('Тип контента'),
        help_text=_('Тип контента'),
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
