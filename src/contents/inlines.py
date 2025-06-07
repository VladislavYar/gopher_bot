from django.contrib import admin

from contents.models import MediaContent, Post, PostType


class MediaContentInline(admin.TabularInline):
    """Inline media-контента."""

    model = MediaContent
    extra = 1


class PostManyToManyInline(admin.TabularInline):
    """Inline постов."""

    model = PostType.posts.through
    verbose_name = Post._meta.verbose_name
    verbose_name_plural = Post._meta.verbose_name_plural
    extra = 1


class PostTypeManyToManyInline(admin.TabularInline):
    """Inline типов постов."""

    model = Post.types.through
    verbose_name = PostType._meta.verbose_name
    verbose_name_plural = PostType._meta.verbose_name_plural
    extra = 1
