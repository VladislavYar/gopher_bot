import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from django.utils import timezone

from constants.bot import CommandEnum, TypeChatEnum
from constants.models import PostTypeEnum
from services.bot.filters import IsAdminFilter
from utils.bot import get_content_post, content_reply_to_message
from utils.user import get_user


router = Router()


@router.message(
    F.chat.type.in_(TypeChatEnum.get_all_group()),
    F.bot,
    F.reply_to_message.from_user.id,
    F.reply_to_message.from_user.username,
    IsAdminFilter(),
    Command(CommandEnum.BAN),
)
async def handler_ban_user(message: Message) -> None:
    """Обработчик блокировки пользователя.

    Args:
        message (Message): сообщение.
    """
    await message.delete()
    await get_user(telegram_id=message.from_user.id, username=message.from_user.username)
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    username = message.reply_to_message.from_user.username
    try:
        await message.bot.ban_chat_member(chat_id, user_id)
        user = await get_user(telegram_id=user_id, username=username)
        user.is_banned = True
        await user.asave()
    except Exception as e:
        logging.error(e)


@router.message(
    F.chat.type.in_(TypeChatEnum.get_all_group()),
    F.bot,
    IsAdminFilter(),
    Command(CommandEnum.UNBAN),
)
async def handler_unban_user(message: Message, command: CommandObject) -> None:
    """Обработчик разблокировки пользователя.

    Args:
        message (Message): сообщение.
        command (CommandObject): объект команды.
    """
    await message.delete()
    await get_user(telegram_id=message.from_user.id, username=message.from_user.username)
    chat_id = message.chat.id
    user_id = username = user = None
    try:
        if (
            message.reply_to_message
            and message.reply_to_message.from_user
            and message.reply_to_message.from_user.id
            and message.reply_to_message.from_user.username
        ):
            user_id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.username
            user = await get_user(telegram_id=user_id, username=username)
        elif username := command.args:
            user = await get_user(username=username)
            user_id = user.telegram_id
        else:
            return
        await message.bot.unban_chat_member(chat_id, user_id)
        user.is_banned = False
        await user.asave()
    except Exception as e:
        logging.error(e)


@router.message(
    F.chat.type.in_(TypeChatEnum.get_all_group()),
    F.reply_to_message,
    F.bot,
    F.from_user.id,
    F.from_user.username,
    Command(CommandEnum.HAPPY),
)
async def handler_happy(message: Message) -> None:
    """Обработчик блокировки пользователя.

    Args:
        message (Message): сообщение.
    """
    await message.delete()
    await get_user(telegram_id=message.from_user.id, username=message.from_user.username)
    audios, images_videos, text, _ = await get_content_post(
        is_published=False,
        types__key=PostTypeEnum.HAPPY,
        datetime_publication__lte=timezone.now(),
    )
    try:
        await content_reply_to_message(message.reply_to_message, audios, images_videos, text)
    except Exception as e:
        logging.error(e)


@router.message(
    F.chat.type.in_(TypeChatEnum.get_all_group()),
    F.reply_to_message,
    F.bot,
    F.from_user.id,
    F.from_user.username,
    Command(CommandEnum.SAD),
)
async def handler_sad(message: Message) -> None:
    """Обработчик блокировки пользователя.

    Args:
        message (Message): сообщение.
    """
    await message.delete()
    await get_user(telegram_id=message.from_user.id, username=message.from_user.username)
    audios, images_videos, text, _ = await get_content_post(
        is_published=False,
        types__key=PostTypeEnum.SAD,
        datetime_publication__lte=timezone.now(),
    )
    try:
        await content_reply_to_message(message.reply_to_message, audios, images_videos, text)
    except Exception as e:
        logging.error(e)


@router.message(
    F.bot,
    F.from_user.id,
    F.from_user.username,
)
async def handler_all_messages(message: Message) -> None:
    """Обработчик всех сообщений.

    Args:
        message (Message): сообщение.
    """
    await get_user(telegram_id=message.from_user.id, username=message.from_user.username)
    type = message.chat.type
    if type == TypeChatEnum.CHANNEL:
        pass
    elif type in TypeChatEnum.get_all_group() and message.reply_to_message:
        pass
    elif type in TypeChatEnum.get_all_group():
        pass
    elif type == TypeChatEnum.PRIVATE:
        pass
