from aiogram import Dispatcher, Bot as TelegramBot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings

from contents.models import Post
from constants.bot import GOOD_MORNING_TIME, GOOD_NIGHT_TIME, INTERVAL_POST_TIME
from services.bot.routers import router
from services.bot.tasks import send_post
from utils.metaclasses import SingletonMeta


class Bot(metaclass=SingletonMeta):
    """Класс telegram-бота."""

    def __init__(self) -> None:
        """Инициализация бота."""
        self.dp = Dispatcher()
        self.dp.include_router(router)
        self.bot = TelegramBot(
            token=settings.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
        )
        self.scheduler = AsyncIOScheduler(timezone=settings.TIME_ZONE)
        self.scheduler.add_job(
            send_post,
            trigger=IntervalTrigger(**INTERVAL_POST_TIME),
            kwargs={'bot': self.bot, 'type': Post.Type.POST},
        )
        self.scheduler.add_job(
            send_post,
            trigger=CronTrigger(**GOOD_MORNING_TIME),
            kwargs={'bot': self.bot, 'type': Post.Type.GOOD_MORNING},
        )
        self.scheduler.add_job(
            send_post,
            trigger=CronTrigger(**GOOD_NIGHT_TIME),
            kwargs={'bot': self.bot, 'type': Post.Type.GOOD_NIGHT},
        )

    async def start(self) -> None:
        """Старт бота и фоновых задач."""
        self.scheduler.start()
        await self.dp.start_polling(self.bot)

    async def stop(self) -> None:
        """Остановка бота и фоновых задач."""
        self.scheduler.shutdown(wait=False)
        await self.dp.stop_polling()
