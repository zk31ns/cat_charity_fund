from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    pass


class DonationDBUser(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBSuperuser(DonationDBUser):
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = None
    user_id: int

    class Config:
        orm_mode = True
