from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import InvestmentBase
from app.repositories.base import CRUDBase


async def invest_funds(
    session: AsyncSession,
    new_obj: InvestmentBase,
    target_crud: CRUDBase,
) -> None:
    """Универсальная функция для инвестирования средств.

    Распределяет средства между новым объектом и открытыми объектами
    противоположного типа (проекты ↔ пожертвования).

    Args:
        session:
            Асинхронная сессия для работы с базой данных.
        new_obj:
            Новый объект для инвестирования (проект или пожертвование).
        target_crud:
            CRUD-репозиторий для поиска открытых объектов, в которые можно
            инвестировать (например, donation_crud при создании проекта,
            или charity_project_crud — при создании пожертвования).
    """
    open_objects = await target_crud.get_open_objects(session)
    await distribute_funds(session, new_obj, open_objects)
    await session.commit()
    await session.refresh(new_obj)


async def distribute_funds(
    session: AsyncSession,
    new_obj: InvestmentBase,
    open_objects: List[InvestmentBase],
) -> None:
    """Распределяет средства между объектами инвестирования.

    Автоматически закрывает объекты (устанавливает флаг `fully_invested`
    и `close_date`), когда они полностью проинвестированы.

    Args:
        session: Асинхронная сессия для работы с базой данных.
        new_obj: Новый объект для инвестирования.
        open_objects: Список открытых объектов (проектов или пожертвований).
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
            obj.close_date = datetime.utcnow()

        required_amount -= investment_amount

    if new_obj.invested_amount == new_obj.full_amount:
        new_obj.fully_invested = True
        new_obj.close_date = datetime.utcnow()
