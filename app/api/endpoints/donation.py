from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import create_new_donation, donations_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationGet
from app.services.investing import invest_donations

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    donation_data = await invest_donations(session, donation)
    return await create_new_donation(donation_data, session, user)


@router.get(
    '/',
    response_model=list[DonationGet],
    response_model_exclude_none=True
)
async def get_donations(
    session: AsyncSession = Depends(get_async_session)
):
    return await donations_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return await donations_crud.get_by_attribute('user_id', user.id, False, session)
