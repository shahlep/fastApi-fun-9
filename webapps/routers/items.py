from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from models import Items, User
from sqlalchemy.orm import Session
from database import get_db
from jose import jwt
from config.settings import Settings
from fastapi.security.utils import get_authorization_scheme_param
from datetime import datetime
from typing import Optional

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/")
def items_home(request: Request, db: Session = Depends(get_db), msg: str = None):
    errors = []
    try:
        token = request.cookies.get("access_token")
        if token is None:
            items = db.query(Items).all()
            return templates.TemplateResponse(
                "items_home_page.html", {"request": request, "items": items, "msg": msg}
            )
        else:
            scheme, param = get_authorization_scheme_param(token)
            payload = jwt.decode(
                param, Settings.SECRET_KEY, algorithms=Settings.ALGORITHM
            )
            email = payload.get("sub")
            user = db.query(User).filter(User.email == email).first()
            items = db.query(Items).filter(Items.owner_id == user.id).all()
            return templates.TemplateResponse(
                "items_home_page.html", {"request": request, "items": items, "msg": msg}
            )
    except Exception:
        errors.append("Something went wrong")
        return templates.TemplateResponse(
            "items_home_page.html",
            {"request": request, "items": items, "errors": errors},
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
async def create_item(request: Request, db: Session = Depends(get_db)):
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
    try:
        token = request.cookies.get("access_token")
        if token is None:
            errors.append("Please login first to create an item")
            return templates.TemplateResponse(
                "create_item_page.html", {"request": request, "errors": errors}
            )
        else:
            scheme, param = get_authorization_scheme_param(token)
            payload = jwt.decode(
                param, Settings.SECRET_KEY, algorithms=Settings.ALGORITHM
            )
            email = payload.get("sub")
            user = db.query(User).filter(User.email == email).first()
            if user is None:
                errors.append(
                    "You are not authenticated.Please login with valid credentials or Create Account."
                )
                return templates.TemplateResponse(
                    "create_item_page.html", {"request": request, "errors": errors}
                )
            else:
                item = Items(
                    title=title,
                    description=description,
                    date_posted=datetime.now().date(),
                    owner_id=user.id,
                )
                db.add(item)
                db.commit()
                db.refresh(item)
                return responses.RedirectResponse(
                    f"/details/{item.id}", status_code=status.HTTP_302_FOUND
                )
    except Exception:
        errors.append("Something went wrong!")
        return templates.TemplateResponse(
            "create_item_page.html", {"request": request, "errors": errors}
        )


@router.get("/delete-an-item")
def show_items_to_delete(request: Request, db: Session = Depends(get_db)):
    errors = []
    token = request.cookies.get("access_token")
    if token is None:
        errors.append("You are not logged in")
        return templates.TemplateResponse(
            "show_item_to_delete_page.html", {"request": request, "errors": errors}
        )
    else:
        try:
            scheme, param = get_authorization_scheme_param(token)
            payload = jwt.decode(
                param, Settings.SECRET_KEY, algorithms=Settings.ALGORITHM
            )
            email = payload.get("sub")
            user = db.query(User).filter(User.email == email).first()
            items = db.query(Items).filter(Items.owner_id == user.id).all()
            return templates.TemplateResponse(
                "show_item_to_delete_page.html",
                {"request": request, "items": items},
            )
        except Exception:
            errors.append("Something went wrong!")
        return templates.TemplateResponse(
            "show_item_to_delete_page.html",
            {"request": request, "items": items, "errors": errors},
        )


@router.get("/search")
def search_item(request: Request, qurey: Optional[str], db: Session = Depends(get_db), msg: str = None):
    return templates.TemplateResponse(
        "items_home_page.html", {"request": request, "msg": msg}
    )
