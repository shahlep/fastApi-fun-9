from pydantic import BaseModel
from pydantic import EmailStr


class User(BaseModel):
    password: str
    email: EmailStr
    is_active: bool


class Items(BaseModel):
    description: str
    title: str
