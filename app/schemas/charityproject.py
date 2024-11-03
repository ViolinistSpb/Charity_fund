from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator


class CharityprojectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = Field(None, example=1000)

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value

    @validator('full_amount')
    def full_amount_cant_be_float(cls, value):
        if isinstance(value, float):
            raise ValueError('Сумма проекта не может быть дробным числом!')
        return value


class CharityprojectCreate(CharityprojectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt = Field(..., example=1000)


class CharityprojectUpdate(CharityprojectBase):
    pass


class CharityprojectDB(CharityprojectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime = Field(None)

    class Config:
        orm_mode = True
