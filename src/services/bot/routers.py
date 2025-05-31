import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from constants.bot import CommandEnum, TypeChatEnum
from services.bot.filters import IsAdminFilter


router = Router()


@router.message(
    F.chat.type.in_(TypeChatEnum.get_all_group()),
    F.reply_to_message.from_user.id,
    F.reply_to_message.from_user.username,
    F.bot,
    IsAdminFilter(),
    Command(CommandEnum.BAN),
)
async def handler_ban_user(message: Message) -> None:
    """Обработчик блокировки пользователя.

    Args:
        message (Message): сообщение.
    """
    await message.delete()
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    try:
        await message.bot.ban_chat_member(chat_id, user_id)
    except Exception as e:
        logging.error(e)


@router.message(
    F.chat.type.in_(TypeChatEnum.get_all_group()),
    F.bot,
    F.reply_to_message.from_user.id,
    F.reply_to_message.from_user.username,
    IsAdminFilter(),
    Command(CommandEnum.UNBAN),
)
async def handler_unban_user(message: Message) -> None:
    """Обработчик разблокировки пользователя.

    Args:
        message (Message): сообщение.
    """
    await message.delete()

    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id

    try:
        await message.bot.unban_chat_member(chat_id, user_id)
    except Exception as e:
        logging.error(e)


@router.message()
async def handler_all_messages(message: Message) -> None:
    """Обработчик всех сообщений.

    Args:
        message (Message): сообщение.
    """
    type = message.chat.type
    if type == TypeChatEnum.CHANNEL:
        pass
    elif type in TypeChatEnum.get_all_group() and message.reply_to_message:
        pass
    elif type in TypeChatEnum.get_all_group():
        pass
    elif type == TypeChatEnum.PRIVATE:
        pass
