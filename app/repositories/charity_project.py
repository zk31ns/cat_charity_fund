from typing import List, Optional

from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Получает ID проекта по имени."""
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_open_projects(
        self,
        session: AsyncSession,
    ) -> List[CharityProject]:
        """Получить незакрытые проекты (для инвестирования)"""
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested.is_(false())
            ).order_by(CharityProject.create_date)
        )
        return projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)