from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)


class CharityProjectUpdate(CharityProjectBase):
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, gt=0)

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: Optional[int] = 0
    fully_invested: Optional[bool] = False
    create_date: datetime = None
    close_date: datetime = None

    class Config:
        orm_mode = True
