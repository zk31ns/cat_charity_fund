from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def invest_funds(
    session: AsyncSession,
    new_obj
) -> None:
    """
    Универсальная функция для инвестирования средств
    между проектами и пожертвованиями
    """
    if isinstance(new_obj, CharityProject):
        open_objects = await get_open_donations(session)
    elif isinstance(new_obj, Donation):
        open_objects = await get_open_projects(session)
    else:
        raise ValueError("Неизвестный тип объекта")

    await distribute_funds(session, new_obj, open_objects)
    await session.commit()
    await session.refresh(new_obj)


async def get_open_projects(session: AsyncSession) -> List[CharityProject]:
    """Получить открытые проекты"""
    from app.crud.charity_project import charity_project_crud
    return await charity_project_crud.get_open_projects(session)


async def get_open_donations(session: AsyncSession) -> List[Donation]:
    """Получить открытые пожертвования"""
    from app.crud.donation import donation_crud
    return await donation_crud.get_open_donations(session)


async def distribute_funds(
    session: AsyncSession,
    new_obj,
    open_objects: List
) -> None:
    """Распределить средства между объектами"""

    required_amount = new_obj.full_amount - new_obj.invested_amount

    for obj in open_objects:
        if required_amount <= 0:
            break

        available_amount = obj.full_amount - obj.invested_amount
        investment_amount = min(available_amount, required_amount)

        obj.invested_amount += investment_amount
        new_obj.invested_amount += investment_amount

        if obj.invested_amount == obj.full_amount:
            obj.fully_invested = True
            obj.close_date = datetime.now()

        required_amount -= investment_amount

    if new_obj.invested_amount == new_obj.full_amount:
        new_obj.fully_invested = True
        new_obj.close_date = datetime.now()