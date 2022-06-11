from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/register")
def user_registration(request: Request):
    return templates.TemplateResponse("user_registration.html", {"request": request})


@router.post("/register")
def register(request: Request):
    pass
