from fastapi import APIRouter
from schemas import ItemCreate

router = APIRouter()


@router.post("/item", tags=["Items"])
def create_item(item:ItemCreate):
    pass
