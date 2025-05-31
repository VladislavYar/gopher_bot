from aiogram.filters import Filter
from aiogram.types import Message


class IsAdminFilter(Filter):
    """Фильтр проверки пользователя на админа."""

    async def __call__(self, message: Message) -> bool:
        """Проверка на админа.

        Args:
            message (Message): сообщение.

        Returns:
            bool: флаг проверка на админа.
        """
        bot = message.bot
        if bot is None:
            return False
        admins = await bot.get_chat_administrators(message.chat.id)
        user = message.from_user
        if not user:
            return False
        return any(admin.user.id == user.id for admin in admins)
