import asyncio

from django.apps import AppConfig
from django_asgi_lifespan.signals import asgi_shutdown


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'
    verbose_name = 'Бот'

    async def stop(self, **kwargs) -> None:
        """Вызывается при остановке приложения."""
        await self.bot.stop()

    def ready(self) -> None:
        """Вызывается при запуске приложения."""
        from services.bot import Bot

        self.bot: Bot = Bot()
        asgi_shutdown.connect(self.stop)
        self.task = asyncio.ensure_future(self.bot.start())
