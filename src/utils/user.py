from constants import MESSAGE_ONE_FIELD_IS_REQUIRED
from constants.utils import MESSAGE_NO_TELEGRAM_USER
from user.models import TelegramUser


async def get_user(
    telegram_id: int | None = None,
    username: str | None = None,
) -> TelegramUser:
    """Отдаёт пользователя telegram. (Создаёт, если нет и обновляет username)

    Args:
        telegram_id (int | None, optional): id пользователя telegram. По дефолту None.
        username (str | None, optional): username пользователя telegram. По дефолту None.

    Raises:
        Exception: Исключение при отсутсвии telegram_id и username.
        Exception: Исключение при отсуствии пользователя telegram.

    Returns:
        TelegramUser: пользователь telegram.
    """
    if telegram_id is None and username is None:
        raise Exception(MESSAGE_ONE_FIELD_IS_REQUIRED)
    if telegram_id:
        user = await TelegramUser.objects.filter(telegram_id=telegram_id).afirst()
        if not user:
            user = await TelegramUser.objects.acreate(telegram_id=telegram_id, username=username)
        if username and user.username != username:
            user.username = username
            await user.asave()
        return user
    user = await TelegramUser.objects.filter(username=username).afirst()
    if user:
        return user
    raise Exception(MESSAGE_NO_TELEGRAM_USER)
