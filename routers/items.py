from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ItemCreate, ShowItem
from models import Items
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime

router = APIRouter()


@router.post("/items", tags=["Items"], response_model=ShowItem)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    owner_id = 1
    date_posted = datetime.now().date()
    item = Items(**item.dict(), date_posted=date_posted, owner_id=owner_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/items/{id}", tags=["Items"],response_model=ShowItem)
def get_item_by_id(id: int, db: Session = Depends(get_db)):
    item = db.query(Items).filter(Items.id == id).first()
    if not item:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Given Item {id} doesn't exist "
        )
    return item
