from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.models.base import InvestmentBase
from app.repositories.charity_project import charity_project_crud
from app.repositories.donation import donation_crud


async def invest_funds(
    session: AsyncSession,
    new_obj: InvestmentBase,
) -> None:
    """Универсальная функция для инвестирования средств.

    Распределяет средства между проектами и пожертвованиями.

    Args:
        session: Асинхронная сессия для работы с базой данных.
        new_obj: Новый объект для инвестирования.

    Note:
        Автоматически определяет тип объекта и выбирает
        открытые объекты для распределения средств.
    """
    if isinstance(new_obj, CharityProject):
        open_objects = await donation_crud.get_open_objects(session)
    else:
        open_objects = await charity_project_crud.get_open_objects(session)

    await distribute_funds(session, new_obj, open_objects)
    await session.commit()
    await session.refresh(new_obj)


async def distribute_funds(
    session: AsyncSession,
    new_obj: InvestmentBase,
    open_objects: List[InvestmentBase],
) -> None:
    """Распределяет средства между объектами инвестирования.

    Args:
        session: Асинхронная сессия для работы с базой данных.
        new_obj: Новый объект для инвестирования.
        open_objects: Список открытых объектов.

    Note:
        Автоматически закрывает объекты, когда они полностью
        инвестированы, устанавливая флаг и дату закрытия.
    """
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
