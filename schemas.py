from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional


class User(BaseModel):
    password: str
    email: EmailStr
    is_active: bool


class Items(BaseModel):
    description: Optional[str]
    title: str
