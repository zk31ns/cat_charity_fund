# app/schemas/charity_project.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator, PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    @validator('description')
    def description_cannot_be_empty(cls, value):
        """Проверяет, что описание не состоит только из пробелов."""
        if not value.strip():
            raise ValueError('Описание не может быть пустым')
        return value


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = None

    @validator('description')
    def description_cannot_be_empty(cls, value):
        """Проверяет, что описание не состоит только из пробелов."""
        if value is not None and not value.strip():
            raise ValueError('Описание не может быть пустым')
        return value

    @validator('name')
    def name_cannot_be_null(cls, value):
        """Проверяет, что название не состоит только из пробелов."""
        if value is not None and not value.strip():
            raise ValueError('Название не может быть пустым')
        return value

    class Config:
        extra = 'forbid'


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True