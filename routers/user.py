from schemas import UserCreate
from sqlalchemy.orm import Session
from hashing import Hash
from fastapi import APIRouter, Depends
from database import get_db
from models import User

router = APIRouter()


@router.get("/user", tags=["User"])
def get_user():
    return {"message": "Hello User"}


@router.post("/create_user", tags=["User"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = User(email=user.email, password=Hash.get_hash_password(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
