from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from models import Items, User
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/")
def items_home(request: Request, db: Session = Depends(get_db), msg: str = None):
    items = db.query(Items).all()
    return templates.TemplateResponse(
        "items_home_page.html", {"request": request, "items": items, "msg": msg}
    )


@router.get("/details/{id}")
def item_details(request: Request, id: int, db: Session = Depends(get_db)):
    item = db.query(Items).filter(Items.id == id).first()
    user = db.query(User).filter(User.id == item.owner_id).first()
    return templates.TemplateResponse(
        "item_details_page.html", {"request": request, "item": item, "user": user}
    )


@router.get("/create-an-item")
def create_item(request: Request):
    return templates.TemplateResponse("create_item_page.html", {"request": request})


@router.post("/create-an-item")
async def create_item(request: Request):
    form = await request.form()
    title = form.get("title")
    description = form.get("description")
    errors = []
    if not title or len(title) < 2:
        errors.append("Title should have at least 2 characters!")
    if not description or len(description) < 10:
        errors.append("Description should have at least 10 characters!")
    if len(errors) > 0:
        return templates.TemplateResponse(
            "create_item_page.html", {"request": request, "errors": errors}
        )
    token = request.cookies.get("access_token")
    if token is None:
        errors.append("Please login first to create an item")
        return templates.TemplateResponse(
            "create_item_page.html", {"request": request, "errors": errors}
        )
