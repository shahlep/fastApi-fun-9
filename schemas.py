from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class ShowUser(BaseModel):
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True


class Items(BaseModel):
    description: Optional[str]
    title: str
