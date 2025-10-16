from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import InvestmentBase
from app.models.user import User


class Donation(InvestmentBase):
    __tablename__ = 'donation'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)

    user = relationship('User', back_populates='donations')