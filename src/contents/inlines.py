from django.contrib import admin

from contents.models import MediaContent


class MediaContentInline(admin.TabularInline):
    """Inline media-контента."""

    model = MediaContent
    extra = 1
