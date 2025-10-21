from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.models.base import InvestmentBase


class Donation(InvestmentBase):
    """Модель пожертвования.

    Attributes:
        user_id: ID пользователя, сделавшего пожертвование.
        comment: Комментарий к пожертвованию.
        user: Связь с пользователем.
    """

    __tablename__ = 'donation'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)
    user = relationship('User', back_populates='donations')

    def __repr__(self) -> str:
        return (
            f"Donation(id={self.id}, user_id={self.user_id}, "
            f"full_amount={self.full_amount}, "
            f"invested_amount={self.invested_amount})"
        )
