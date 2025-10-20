from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import PositiveInt

from app.models.charity_project import CharityProject


async def check_charity_project_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Название проекта уникально."""
    from app.repositories.charity_project import charity_project_crud

    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Существование проекта."""
    from app.repositories.charity_project import charity_project_crud

    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


async def check_charity_project_before_delete(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """
    Возможность удаления проекта.
    Нельзя удалить если уже внесены средства.
    """
    project = await check_charity_project_exists(project_id, session)

    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, нельзя удалять!'
        )

    return project


async def check_charity_project_before_update(
    project_id: int,
    session: AsyncSession,
    full_amount: PositiveInt
) -> CharityProject:
    """
    Обновление проекта.
    Нельзя обновлять закрытые проекты и устанавливать сумму меньше внесенной.
    """
    project = await check_charity_project_exists(project_id, session)

    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )

    if full_amount is not None and full_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя установить требуемую сумму меньше уже внесенной!'
        )

    return project