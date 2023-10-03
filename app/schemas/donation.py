from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: int = Field(..., gt=0)


class DonationCreate(DonationBase):
    ...


class DonationDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationGet(DonationBase):
    id: int
    create_date: datetime
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: datetime = None
    user_id: Optional[int] = None

    class Config:
        orm_mode = True