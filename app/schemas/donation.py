from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    """Базовая схема для пожертвования.

    Attributes:
        full_amount: Сумма пожертвования (положительное число).
        comment: Комментарий к пожертвованию (опционально).
    """
    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    """Схема для создания нового пожертвования."""


class DonationDBUser(DonationBase):
    """Схема для отображения пожертвований пользователю.

    Содержит только те поля, которые разрешено видеть обычному пользователю.

    Attributes:
        id: Уникальный идентификатор пожертвования.
        create_date: Дата создания пожертвования.
    """
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBSuperuser(DonationDBUser):
    """Схема для отображения полной информации о пожертвовании.

    Содержит все поля, включая служебные, доступные только суперпользователям.

    Attributes:
        invested_amount: Уже инвестированная сумма.
        fully_invested: Флаг полного инвестирования.
        close_date: Дата закрытия инвестирования.
        user_id: Идентификатор пользователя, сделавшего пожертвование.
    """
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = None
    user_id: int

    class Config:
        orm_mode = True