from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class ShowUser(BaseModel):
    email: EmailStr
    is_active: bool = True

    class Config:
        orm_mode = True


class ItemCreate(BaseModel):
    description: Optional[str]
    title: str
