from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings

from constants.bot import INTERVAL_POST_TIME
from services.bot.routers import router
from services.bot.tasks import send_post_by_channel
from utils.bot import get_bot
from utils.metaclasses import SingletonMeta


class Bot(metaclass=SingletonMeta):
    """Класс telegram-бота."""

    def __init__(self) -> None:
        """Инициализация бота."""
        self.dp = Dispatcher()
        self.dp.include_router(router)
        self.bot = get_bot()
        self.scheduler = AsyncIOScheduler(
            timezone=settings.TIME_ZONE,
            jobstores=settings.SCHEDULER_JOBSTORES,
        )
        self.scheduler.add_job(
            send_post_by_channel,
            trigger=IntervalTrigger(**INTERVAL_POST_TIME),
        )

    async def start(self) -> None:
        """Старт бота и фоновых задач."""
        self.scheduler.start()
        await self.dp.start_polling(self.bot)

    async def stop(self) -> None:
        """Остановка бота и фоновых задач."""
        if self.scheduler.running:
            self.scheduler.shutdown()
        await self.dp.stop_polling()
