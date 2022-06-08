from fastapi import APIRouter, Depends
from schemas import ItemCreate
from models import Items
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime

router = APIRouter()


@router.post("/item", tags=["Items"])
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    owner_id = 1
    date_posted = datetime.date()
    item = Items(**item.dict(), date_posted=date_posted, owner_id=owner_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
