class SingletonMeta(type):
    """Метакласс, реализующий функционал паттерна синглтон.

    Attributes:
        _instances (dict[type: object]): словарь для хранения уже созданных объектов классов.
    """

    _instances: dict[type, object] = {}

    def __call__(cls: type, *args, **kwargs) -> object:
        """Создаёт объект класса или отдаёт уже созданный.

        Args:
            cls (type): класс создаваемого или созданного объекта.

        Returns:
            object: созданный объект.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
