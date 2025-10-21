from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.models import User
from app.repositories.charity_project import charity_project_crud
from app.repositories.donation import donation_crud
from app.schemas.donation import (
    DonationCreate,
    DonationDBUser,
    DonationDBSuperuser,
)
from app.services.investment import invest_funds

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDBUser,
    response_model_exclude_none=True,
    summary='Создать пожертвование'
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Создать пожертвование."""
    new_donation = await donation_crud.create(
        donation, session, user=user
    )
    await invest_funds(session, new_donation, charity_project_crud)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDBUser],
    response_model_exclude_none=True,
    summary='Получить мои пожертвования'
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получить список моих пожертвований."""
    return await donation_crud.get_by_user(session, user)


@router.get(
    '/',
    response_model=list[DonationDBSuperuser],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Получить все пожертвования'
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Получить все пожертвования (только для суперпользователя)."""
    return await donation_crud.get_multi(session)
