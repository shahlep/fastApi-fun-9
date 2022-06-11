from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/")
def items_home(request: Request):
    return templates.TemplateResponse("items_home_page.html", {"request": request})
