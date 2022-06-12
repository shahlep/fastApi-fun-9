from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db

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
