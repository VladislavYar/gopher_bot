from aiogram import Dispatcher
from aiogram.types import Message


dp = Dispatcher()


@dp.message()
async def handler_all_messages(message: Message) -> None:
    """Обработчик всех сообщений.

    Args:
        message (Message): сообщение.
    """
    pass
