from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User

donations_crud = CRUDBase(Donation)


async def create_new_donation(
        donation_data: dict,
        session: AsyncSession,
        user: Optional[User] = None
):
    if user is not None:
        donation_data['user_id'] = user.id
    db_donation = Donation(**donation_data)
    session.add(db_donation)
    await session.commit()
    await session.refresh(db_donation)
    return db_donation
