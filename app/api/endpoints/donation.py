from typing import List
from fastapi import APIRouter, Depends
# Импортируем класс асинхронной сессии для аннотации параметра.
from sqlalchemy.ext.asyncio import AsyncSession

# Импортируем асинхронный генератор сессий.
from app.core.db import get_async_session
# from app.crud.meeting_room import meeting_room_crud
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate, DonationDB, DonationBase, AllDonationsDB
)
# from app.api.validators import check_meeting_room_exists, check_name_duplicate
from app.core.user import current_superuser, current_user
from app.models import User
from app.services.funds_allocation import invested_donation


router = APIRouter()


@router.post(
    '/',
    # Указываем схему ответа.
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        # Указываем зависимость, предоставляющую объект сессии, как параметр функции.
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    # await check_name_duplicate(meeting_room.name, session)
    new_donation = await donation_crud.create(donation, session, user)
    await invested_donation(session, new_donation)
    return new_donation


@router.get(
    '/',
    response_model=List[AllDonationsDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Просмотр всех донатов только для суперюзеров"""
    all_donatioms = await donation_crud.get_multi(session)
    return all_donatioms


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получает список всех донатов для текущего пользователя."""
    reservations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return reservations
