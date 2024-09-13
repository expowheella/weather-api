from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional


class CityBase(BaseModel):
    name: str


class CityGet(CityBase):
    city_id: int

    class Config:
        orm_mode = True
