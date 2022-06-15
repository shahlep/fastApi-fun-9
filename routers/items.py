from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ItemCreate, ShowItem
from models import Items, User
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from .login import oauth_scheme
from jose import jwt
from config.settings import Settings

router = APIRouter()


def get_user_from_token(token, db):
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=Settings.ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to verify credentials!",
            )
        user = db.query(User).filter(User.email == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to verify credentials!",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to verify credentials!",
        )
    return user


@router.post("/items", tags=["Items"], response_model=ShowItem)
def create_item(
    item: ItemCreate, db: Session = Depends(get_db), token: str = Depends(oauth_scheme)
):
    user = get_user_from_token(token, db)
    owner_id = user.id
    date_posted = datetime.now().date()
    item = Items(**item.dict(), date_posted=date_posted, owner_id=owner_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/items/all", tags=["Items"], response_model=List[ShowItem])
def get_all_items(db: Session = Depends(get_db)):
    item = db.query(Items).all()
    return item


@router.get("/items/{id}", tags=["Items"], response_model=ShowItem)
def get_item_by_id(id: int, db: Session = Depends(get_db)):
    item = db.query(Items).filter(Items.id == id).first()
    if not item:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Given Item {id} doesn't exist "
        )
    return item


@router.put("/items/update/{id}", tags=["Items"])
def update_item_by_id(
    id: int,
    item: ItemCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth_scheme),
):
    user = get_user_from_token(token, db)
    existing_item = db.query(Items).filter(Items.id == id)
    if not existing_item.first():
        return {"Message": f"Item with id {id} doesn't exist!"}
    if existing_item.first().owner_id == user.id:
        existing_item.update(
            jsonable_encoder(item)
        )  # or use- existing_item.update(item.__dict__)
        db.commit()
        return {"Message": f"Item information with id {id} has been updated!"}
    else:
        return {"Message": f"You are not autorized to update this item!"}


@router.delete("/items/delete/{id}", tags=["Items"])
def delete_item_by_id(
    id: int, db: Session = Depends(get_db), token: str = Depends(oauth_scheme)
):
    user = get_user_from_token(token, db)
    existing_item = db.query(Items).filter(Items.id == id)
    if not existing_item.first():
        return {"Message": f"Item with id {id} doesn't exist!"}
    if existing_item.first().owner_id == user.id:
        existing_item.delete()
        db.commit()
        return {"Message": f"Item with id {id} successfully deleted!"}
    else:
        return {"Message": f"You are not authorized!"}


def autocomplete(term: Optional[str], db: Session = Depends(get_db)):
    items = db.query(Items).filter(Items.title.contains(term)).all()
    suggestions = []
    for item in items:
        suggestions.append(item)
    return suggestions

