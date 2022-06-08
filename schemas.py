from pydantic import BaseModel
from pydantic import EmailStr
from datetime import date


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class ShowUser(BaseModel):
    email: EmailStr
    is_active: bool = True

    class Config:
        orm_mode = True


class ItemCreate(BaseModel):
    title: str
    description: str


class ShowItem(BaseModel):
    title: str
    description: str
    date_posted: date

    class Config:
        orm_mode = True
