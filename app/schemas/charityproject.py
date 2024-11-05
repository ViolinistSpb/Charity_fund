from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator, Extra

from app.constants import (FULL_AMOUNT_EXAMPLE, MIN_NAME_LENGTH,
                           MAX_NAME_LENGTH, MIN_DESCRIPTION_LENGTH)


class CharityprojectBase(BaseModel):
    name: Optional[str] = Field(
        None, min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH
    )
    description: Optional[str] = Field(None, min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: Optional[PositiveInt] = Field(
        None, example=FULL_AMOUNT_EXAMPLE
    )

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
    name: str = Field(
        ..., min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH
    )
    description: str = Field(..., min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: PositiveInt = Field(..., example=FULL_AMOUNT_EXAMPLE)

    class Config:
        extra = Extra.forbid


class CharityprojectUpdate(CharityprojectBase):

    class Config:
        extra = Extra.forbid


class CharityprojectDB(CharityprojectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime = Field(None)

    class Config:
        orm_mode = True
