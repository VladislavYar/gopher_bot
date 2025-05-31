from aiogram import Bot as TelegramBot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings

from services.bot.dispatcher import dp
from services.bot.tasks import send_post
from utils.metaclasses import SingletonMeta


class Bot(metaclass=SingletonMeta):
    """Класс telegram-бота."""

    def __init__(self) -> None:
        """Инициализация бота."""
        self.bot = TelegramBot(
            token=settings.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
        )
        self.scheduler = AsyncIOScheduler(timezone=settings.TIME_ZONE)
        self.scheduler.add_job(
            send_post,
            trigger=IntervalTrigger(seconds=1),
            kwargs={'bot': self.bot},
        )

    async def start(self) -> None:
        """Старт бота и фоновых задач."""
        self.scheduler.start()
        await dp.start_polling(self.bot)

    async def stop(self) -> None:
        """Остановка бота и фоновых задач."""
        self.scheduler.shutdown(wait=False)
        await dp.stop_polling()
