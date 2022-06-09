from schemas import UserCreate, ShowUser
from sqlalchemy.orm import Session
from hashing import Hash
from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from models import User
from typing import List

router = APIRouter()


@router.get("/users", tags=["User"], response_model=List[ShowUser])
def get_all_user(db: Session = Depends(get_db)):
    user = db.query(User).all()
    return user


@router.get("/users/{id}", tags=["User"], response_model=List[ShowUser])
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"User id {id} doesn't exist "
        )
    return user


@router.post("/users", tags=["User"], response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = User(email=user.email, password=Hash.get_hash_password(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
