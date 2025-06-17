import logging

from asgiref.sync import async_to_sync
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.core.handlers.asgi import ASGIRequest
from django.forms import ModelForm

from user.models import TelegramUser
from utils.bot import get_bot


admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    """Админ-панель пользователей telegram."""

    list_display = ('id', 'telegram_id', 'username', 'is_banned')
    search_fields = ('telegram_id', 'username')
    list_filter = ('is_banned',)

    def check_is_banned(self, obj: TelegramUser) -> None:
        """Проверка блокировки и разблокировки пользователя telegram.

        Args:
            obj (TelegramUser): пользователь telegram.
        """
        bot = get_bot()
        chat_id = settings.BOT_CHAT
        user_id = obj.telegram_id
        try:
            if obj.is_banned:
                async_to_sync(bot.ban_chat_member)(chat_id, user_id)
            else:
                async_to_sync(bot.unban_chat_member)(chat_id, user_id)
        except Exception as e:
            logging.error(e)

    def save_form(self, request: ASGIRequest, form: ModelForm, change: bool) -> TelegramUser:
        """Сохранение формы пользователя telegram.

        Args:
            request (ASGIRequest): запрос к серверу.
            form (ModelForm): форма.
            change (bool): флаг изменения.

        Returns:
            TelegramUser: пользователь telegram.
        """
        obj = form.save(commit=False)
        self.check_is_banned(obj)
        return obj

    def save_model(self, request: ASGIRequest, obj: TelegramUser, form: ModelForm, change: bool) -> None:
        """Сохранение пользователя telegram.

        Args:
            request (ASGIRequest): запрос к серверу.
            obj (TelegramUser): пользователь telegram.
            form (ModelForm): форма.
            change (bool): флаг изменения.
        """
        obj.save()
        self.check_is_banned(obj)
