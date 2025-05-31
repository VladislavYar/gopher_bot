from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import SafeString

from contents.models import Post, MediaContent
from contents.inlines import MediaContentInline
from constants.admin import SIZE_MEDIA_CONTENT


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Админ-панель постов."""

    list_display = ('id', 'title', 'is_published')
    list_editable = ('title', 'is_published')
    search_fields = ('title',)
    list_filter = ('is_published',)

    inlines = (MediaContentInline,)


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
                f'<img src="{url}" style="max-width:{SIZE_MEDIA_CONTENT}px; max-height:{SIZE_MEDIA_CONTENT}px"/>',
            )
        elif obj.type == MediaContent.Type.VIDEO:
            return format_html(
                f'<video controls width="{SIZE_MEDIA_CONTENT}" height="{SIZE_MEDIA_CONTENT}" src="{url}"></video>',
            )
        return format_html(f'<audio controls src="{url}"></audio>')
