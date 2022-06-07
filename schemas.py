from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Items(BaseModel):
    description: Optional[str]
    title: str
