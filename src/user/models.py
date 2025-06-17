from django.db import models
from django.utils.translation import gettext_lazy as _


class TelegramUser(models.Model):
    """Модель пользователь telegram."""

    telegram_id = models.BigIntegerField(
        db_index=True,
        unique=True,
        verbose_name=_('Id пользователя telegram'),
        help_text=_('Id пользователя telegram'),
        db_comment=_('Id пользователя telegram'),
    )
    username = models.SlugField(
        db_index=True,
        blank=True,
        null=True,
        verbose_name=_('Username пользователя telegram'),
        help_text=_('Username пользователя telegram'),
        db_comment=_('Username пользователя telegram'),
    )
    is_banned = models.BooleanField(
        default=False,
        verbose_name=_('Флаг блокировки пользователя telegram'),
        help_text=_('Флаг блокировки пользователя telegram'),
        db_comment=_('Флаг блокировки пользователя telegram'),
    )

    def __str__(self) -> str:
        return f'{self.pk}-{self.telegram_id}-{self.username}'

    class Meta:
        verbose_name = _('Пользователь telegram')
        verbose_name_plural = _('Пользователи telegram')
