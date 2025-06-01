from enum import StrEnum


GOOD_MORNING_TIME = {'hour': 7}
GOOD_NIGHT_TIME = {'hour': 20}
INTERVAL_POST_TIME = {'minutes': 1}


class TypeChatEnum(StrEnum):
    """Enum типа чата."""

    GROUP = 'group'
    SUPERGRUP = 'supergroup'
    CHANNEL = 'channel'
    PRIVATE = 'private'

    @classmethod
    def get_all_group(cls) -> tuple[str, str]:
        """Отдаёт типы всех групп.

        Returns:
            tuple[str, str]: типы всех групп.
        """
        return cls.GROUP, cls.SUPERGRUP


class CommandEnum(StrEnum):
    """Enum команд канала."""

    BAN = 'ban'
    UNBAN = 'unban'
    HAPPY = 'happy'
    SAD = 'sad'
