from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase[CharityProject]):
    """CRUD операции для благотворительных проектов."""

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Получает ID проекта по имени."""
        project = await self.get_one_by_attributes(session, name=project_name)
        return project.id if project else None


charity_project_crud = CRUDCharityProject(CharityProject)
