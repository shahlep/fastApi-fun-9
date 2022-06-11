from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
def items_home():
    return templates.TemplateResponse("item_home_page.html")
