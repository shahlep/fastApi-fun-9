from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from models import Items
from sqlalchemy.orm import Session

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/")
def items_home(request: Request,db:Session):
    items = db.query(Items).all()
    return templates.TemplateResponse("items_home_page.html", {"request": request})
