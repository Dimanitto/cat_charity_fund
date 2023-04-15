from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    # comment: Optional[str]
    # full_amount: int
    create_date: datetime

    class Config:
        orm_mode = True


class AllDonationsDB(DonationDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
