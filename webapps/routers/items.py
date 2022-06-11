from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
def items_home(request: Request):
    return templates.TemplateResponse("item_home_page.html", {"request": request})
