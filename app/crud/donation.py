from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    """CRUD операции для пожертвований"""

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User
    ) -> List[Donation]:
        """Получить пожертвования конкретного пользователя"""
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()

    async def get_open_donations(
        self,
        session: AsyncSession,
    ) -> List[Donation]:
        """Получить незакрытые пожертвования (для инвестирования)"""
        donations = await session.execute(
            select(Donation).where(
                Donation.fully_invested == False
            ).order_by(Donation.create_date)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)