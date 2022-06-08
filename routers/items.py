from fastapi import APIRouter, Depends
from schemas import ItemCreate, ShowItem
from models import Items
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime

router = APIRouter()


@router.post("/item", tags=["Items"], response_model=ShowItem)
def create_item(item: ItemCreate, user_id: int, db: Session = Depends(get_db)):
    date_posted = datetime.now().date()
    item = Items(**item.dict(), date_posted=date_posted, owner_id=user_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
