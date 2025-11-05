from typing import Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DAYS_IN_YEAR, DAYS_IN_MONTH
from app.core.investing import distribute_funds
from app.models import User
from app.models.charity_project import CharityProject
from app.repositories.base import CRUDBase
from app.schemas.charity_project import CharityProjectCreate


class CRUDCharityProject(CRUDBase[CharityProject]):
    """CRUD операции для благотворительных проектов."""

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        project = await self.get_one_by_attributes(session, name=project_name)
        return project.id if project else None

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:
        year_diff = (
            extract('year', CharityProject.close_date) -
            extract('year', CharityProject.create_date)
        ) * DAYS_IN_YEAR
        month_diff = (
            extract('month', CharityProject.close_date) -
            extract('month', CharityProject.create_date)
        ) * DAYS_IN_MONTH
        day_diff = (
            extract('day', CharityProject.close_date) -
            extract('day', CharityProject.create_date)
        )

        days_to_complete = year_diff + month_diff + day_diff

        statement = select(CharityProject).where(
            CharityProject.fully_invested.is_(True)
        ).order_by(
            days_to_complete
        )

        result = await session.execute(statement)
        return result.scalars().all()

    async def get_closed_projects_count(
        self,
        session: AsyncSession,
    ) -> int:
        statement = select(CharityProject).where(
            CharityProject.fully_invested.is_(True)
        )
        result = await session.execute(statement)
        return len(result.scalars().all())

    async def create_and_invest(
        self,
        *,
        session: AsyncSession,
        obj_in: CharityProjectCreate,
        user: Optional[User] = None,
        opposite_crud=None,
    ) -> CharityProject:
        open_donations = await opposite_crud.get_open_objects(session)
        new_project = await self.create(
            obj_in=obj_in,
            session=session,
            user=user,
            commit=False
        )

        await distribute_funds(session, new_project, open_donations)
        await session.commit()
        await session.refresh(new_project)
        return new_project


charity_project_crud = CRUDCharityProject(CharityProject)