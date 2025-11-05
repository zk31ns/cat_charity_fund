from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.investing import distribute_funds
from app.repositories.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase[Donation]):
    """CRUD операции для пожертвований."""

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User
    ) -> List[Donation]:
        """Получить пожертвования конкретного пользователя."""
        return await self.get_by_attributes(session, user_id=user.id)

    async def create_and_invest(
        self,
        *,
        session: AsyncSession,
        obj_in: DonationCreate,
        user: Optional[User] = None,
        opposite_crud=None,
    ) -> Donation:
        open_projects = await opposite_crud.get_open_objects(session)
        new_donation = await self.create(
            obj_in=obj_in,
            session=session,
            user=user,
            commit=False
        )

        await distribute_funds(session, new_donation, open_projects)
        await session.commit()
        await session.refresh(new_donation)

        return new_donation


donation_crud = CRUDDonation(Donation)