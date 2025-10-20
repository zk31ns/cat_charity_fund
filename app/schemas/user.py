from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема для чтения данных пользователя.

    Наследует все стандартные поля от BaseUser.
    Используется для возврата данных пользователю.
    """


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания нового пользователя.

    Наследует все стандартные поля от BaseUserCreate.
    Используется при регистрации нового пользователя.
    """


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления данных пользователя.

    Наследует все стандартные поля от BaseUserUpdate.
    Используется для изменения данных существующего пользователя.
    """
