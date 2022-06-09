from schemas import UserCreate, ShowUser
from sqlalchemy.orm import Session
from hashing import Hash
from fastapi import APIRouter, Depends
from database import get_db
from models import User
from typing import List

router = APIRouter()


@router.get("/users", tags=["User"], response_model=List[ShowUser])
def get_all_user(db: Session = Depends(get_db)):
    user = db.query(User).all()
    return user


@router.post("/users", tags=["User"], response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = User(email=user.email, password=Hash.get_hash_password(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
