from typing import List

from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase[Donation]):
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
                Donation.fully_invested.is_(false())
            ).order_by(Donation.create_date)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)