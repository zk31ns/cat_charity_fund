from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    """Базовая схема для благотворительного проекта.

    Attributes:
        name: Название проекта (от 1 до 100 символов).
        description: Описание проекта (не может быть пустым).
        full_amount: Требуемая сумма для проекта (положительное число).
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    @validator('description')
    def description_cannot_be_empty(cls, value):
        """Проверяет, что описание не состоит только из пробелов.

        Args:
            value: Значение поля description.

        Returns:
            str: Проверенное значение.

        Raises:
            ValueError: Если описание состоит только из пробелов.
        """
        if not value.strip():
            raise ValueError('Описание не может быть пустым')
        return value


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания нового благотворительного проекта."""


class CharityProjectUpdate(BaseModel):
    """Схема для обновления благотворительного проекта.

    Attributes:
        name: Новое название проекта (опционально).
        description: Новое описание проекта (опционально).
        full_amount: Новая требуемая сумма (опционально).
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = None

    @validator('description')
    def description_cannot_be_empty(cls, value):
        """Проверяет, что описание не состоит только из пробелов.

        Args:
            value: Значение поля description.

        Returns:
            Optional[str]: Проверенное значение или None.

        Raises:
            ValueError: Если описание состоит только из пробелов.
        """
        if value is not None and not value.strip():
            raise ValueError('Описание не может быть пустым')
        return value

    @validator('name')
    def name_cannot_be_null(cls, value):
        """Проверяет, что название не состоит только из пробелов.

        Args:
            value: Значение поля name.

        Returns:
            Optional[str]: Проверенное значение или None.

        Raises:
            ValueError: Если название состоит только из пробелов.
        """
        if value is not None and not value.strip():
            raise ValueError('Название не может быть пустым')
        return value

    class Config:
        extra = 'forbid'


class CharityProjectDB(CharityProjectBase):
    """Схема для отображения данных благотворительного проекта.

    Attributes:
        id: Уникальный идентификатор проекта.
        invested_amount: Уже инвестированная сумма.
        fully_invested: Флаг полного инвестирования.
        create_date: Дата создания проекта.
        close_date: Дата закрытия проекта (если инвестирован полностью).
    """
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True