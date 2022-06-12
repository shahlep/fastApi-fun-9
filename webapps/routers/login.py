from fastapi import APIRouter, Request, Depends
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import User
from hashing import Hash
from jose import jwt
from config.settings import Settings

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    errors = []
    if not email:
        errors.append("Please enter valid email!")
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": errors}
        )
    if len(password) > 6:
        errors.append("Password should be at least 6 characters!")
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": errors}
        )
    try:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            errors.append("Email doesn't exist!")
            return templates.TemplateResponse(
                "login.html", {"request": request, "errors": errors}
            )
        else:
            if Hash.verify_password(password, User.password):
                data = {"sub": email}
                jwt_token = jwt.encode(
                    data, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM
                )
                Response.set_cookie(
                    key="access_token", value=f"Bearer {jwt_token}", httponly=True
                )
                msg = "Login Successful!"
                return templates.TemplateResponse(
                    "login.html", {"request": request, "errors": errors,"msg":msg}
                )
            else:
                errors.append("Invalid password!")
                return templates.TemplateResponse(
                    "login.html", {"request": request, "errors": errors}
                )
    except Exception:
        errors.append("something went wrong!")
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": errors}
        )
