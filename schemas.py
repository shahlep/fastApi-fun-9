from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional


class UserCreate(BaseModel):
    password: str
    email: EmailStr


class Items(BaseModel):
    description: Optional[str]
    title: str
