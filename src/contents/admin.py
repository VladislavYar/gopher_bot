from admin_extra_buttons.api import button
from admin_extra_buttons.mixins import ExtraButtonsMixin
from asgiref.sync import async_to_sync
from django.contrib import admin, messages
from django.core.handlers.asgi import ASGIRequest
from django.utils.html import format_html
from django.utils.encoding import force_str
from django.utils.safestring import SafeString
from django.utils import timezone

from contents.models import PostType, Post, MediaContent
from contents.inlines import PostTypeManyToManyInline, PostManyToManyInline, MediaContentInline
from constants.admin import (
    SIZE_MEDIA_CONTENT,
    BUTTON_LABEL_SEND_POST,
    MESSAGE_NO_SEND_POST,
    MESSAGE_SEND_POST,
    MESSAGE_POST_IS_PUBLISHED,
    MESSAGE_POST_NOT_TIME_PUBLICATION,
    MESSAGE_POST_TYPE_NOT_POST,
)
from constants.models import PostTypeEnum
from utils.bot import get_content_post, get_bot, send_post_by_channel


@admin.register(Post)
class PostAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    """Админ-панель постов."""

    list_display = ('id', 'title', 'is_published', 'datetime_publication')
    list_editable = ('title', 'is_published', 'datetime_publication')
    search_fields = ('title',)
    list_filter = ('is_published', 'types')

    inlines = (MediaContentInline, PostTypeManyToManyInline)

    @button(label=BUTTON_LABEL_SEND_POST)
    def send_post_by_channel(self, request: ASGIRequest, pk: int) -> None:
        """Опубликовать пост в канал.

        Args:
            request (ASGIRequest): запрос к серверу.
            pk (int): первичный ключ поста.
        """
        obj: Post = self.get_object(request, pk)
        errors = []
        if obj.is_published:
            errors.append(MESSAGE_POST_IS_PUBLISHED)
        if obj.datetime_publication > timezone.now():
            errors.append(MESSAGE_POST_NOT_TIME_PUBLICATION)
        if PostTypeEnum.POST not in obj.types.all().values_list('key', flat=True):
            errors.append(MESSAGE_POST_TYPE_NOT_POST.format(PostTypeEnum.POST))
        if errors:
            self.message_user(
                request, MESSAGE_NO_SEND_POST.format(', '.join(force_str(e) for e in errors)), level=messages.ERROR
            )
            return
        try:
            audios, images_videos, text, _ = async_to_sync(get_content_post)(pk=obj.pk)
            async_to_sync(send_post_by_channel)(bot=get_bot(), audios=audios, images_videos=images_videos, text=text)
            obj.is_published = True
            obj.save()
            self.message_user(request, MESSAGE_SEND_POST)
        except Exception as e:
            self.message_user(request, MESSAGE_NO_SEND_POST.format(e), level=messages.ERROR)


@admin.register(PostType)
class PostTypeAdmin(admin.ModelAdmin):
    """Админ-панель типов постов."""

    list_display = (
        'id',
        'title',
        'key',
        'time_publication',
        'is_publish_by_cron',
        'is_publish_by_command',
        'is_publish_by_admin',
    )
    list_editable = (
        'title',
        'key',
        'time_publication',
        'is_publish_by_cron',
        'is_publish_by_command',
        'is_publish_by_admin',
    )
    search_fields = ('title', 'key')
    list_filter = ('title', 'key')

    inlines = (PostManyToManyInline,)


@admin.register(MediaContent)
class MediaContentAdmin(admin.ModelAdmin):
    """Админ-панель media-контента."""

    list_display = ('id', 'post', 'html_content', 'type')
    fields = ('id', 'post', 'type', 'content', 'html_content')
    readonly_fields = (
        'id',
        'html_content',
    )
    autocomplete_fields = ('post',)
    list_filter = ('type',)
    list_select_related = ('post',)

    def html_content(self, obj: MediaContent) -> SafeString:
        """Отдаёт media-контент в виде HTML.

        Args:
            obj (MediaContent): объект media-контента.

        Returns:
            SafeString: media-контент в виде HTML.
        """
        url = obj.content.url
        if obj.type == MediaContent.Type.IMAGE:
            return format_html(
                '<img src="{}" style="max-width:{}px; max-height:{}px"/>',
                url,
                SIZE_MEDIA_CONTENT,
                SIZE_MEDIA_CONTENT,
            )
        elif obj.type == MediaContent.Type.VIDEO:
            return format_html(
                '<video controls width="{}" height="{}" src="{}"></video>',
                SIZE_MEDIA_CONTENT,
                SIZE_MEDIA_CONTENT,
                url,
            )
        return format_html('<audio controls src="{}"></audio>', url)
