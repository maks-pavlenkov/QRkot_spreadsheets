import datetime
from sqlalchemy import Column, Integer, Boolean, Text, DateTime, ForeignKey
from app.core.db import Base


class Donation(Base):
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.datetime.now)
    close_date = Column(DateTime)
