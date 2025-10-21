from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase[Donation]):
    """CRUD операции для пожертвований."""

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User
    ) -> List[Donation]:
        """Получить пожертвования конкретного пользователя."""
        return await self.get_by_attributes(session, user_id=user.id)


donation_crud = CRUDDonation(Donation)
