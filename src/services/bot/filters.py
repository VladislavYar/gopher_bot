from aiogram.filters import Filter
from aiogram.types import Message

from utils.bot import check_is_admin


class IsAdminFilter(Filter):
    """Фильтр проверки пользователя на админа."""

    async def __call__(self, message: Message) -> bool:
        """Проверка на админа.

        Args:
            message (Message): сообщение.

        Returns:
            bool: флаг проверка на админа.
        """
        return await check_is_admin(message)
