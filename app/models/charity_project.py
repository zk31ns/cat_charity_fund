from sqlalchemy import Column, String, Text

from app.models.base import InvestmentBase


class CharityProject(InvestmentBase):
    """Модель благотворительного проекта.

    Attributes:
        name: Название проекта (уникальное)
        description: Описание проекта.
    """
    __tablename__ = 'charityproject'

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return (
            f"CharityProject(id={self.id}, name='{self.name}', "
            f"full_amount={self.full_amount}, "
            f"invested_amount={self.invested_amount})"
        )