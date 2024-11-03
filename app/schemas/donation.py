from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator


class DonationBase(BaseModel):
    comment: Optional[str] = Field(None)
    full_amount: PositiveInt = Field(..., example=1000)

    @validator('full_amount')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError(
                'Целевая сумма пожертвования не может быть пустой!'
            )
        return value


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime = Field(None)
    user_id: Optional[int]

    class Config:
        orm_mode = True