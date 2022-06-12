from fastapi import APIRouter, Request, Depends, responses,status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from hashing import Hash
from models import User
from sqlalchemy.exc import IntegrityError

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/register")
def user_registration(request: Request):
    return templates.TemplateResponse("user_registration.html", {"request": request})


@router.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    errors = []
    user = User(email=email, password=Hash.get_hash_password(password))
    if len(password) < 6:
        errors.append("Password should be at least 6 characters!")
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        responses.RedirectResponse("/?msg=Successfully Registered!",status_code=status.HTTP_302_FOUND)
    except IntegrityError:
        errors.append("Email already exists")
        return templates.TemplateResponse("user_registration.html", {"request": request, "errors": errors})
