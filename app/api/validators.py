# app/api/validators.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject


async def check_charity_project_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверяет, что название проекта уникально."""
    from app.crud.charity_project import charity_project_crud

    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверяет, что проект существует."""
    from app.crud.charity_project import charity_project_crud

    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return project


async def check_charity_project_before_delete(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """
    Проверяет можно ли удалить проект.
    Нельзя удалить если уже внесены средства.
    """
    # from app.crud.charity_project import charity_project_crud

    project = await check_charity_project_exists(project_id, session)

    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, нельзя удалять!'
        )

    return project


async def check_charity_project_before_update(
    project_id: int,
    session: AsyncSession,
    full_amount: int = None,
) -> CharityProject:
    """
    Проверяет можно ли обновить проект.
    Нельзя обновлять закрытые проекты и устанавливать сумму меньше внесенной.
    """
    project = await check_charity_project_exists(project_id, session)

    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )

    if full_amount is not None and full_amount < project.invested_amount:
        raise HTTPException(
            status_code=422,
            detail='Нельзя установить требуемую сумму меньше уже внесенной!'
        )

    return project