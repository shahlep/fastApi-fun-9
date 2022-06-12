from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from hashing import Hash
from models import User

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
    user = User(email=email, password=Hash.get_hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
