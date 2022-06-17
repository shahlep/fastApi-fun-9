from fastapi import APIRouter, Request, Depends, responses, status, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import User
from hashing import Hash
from jose import jwt
from config.settings import Settings
from routers.login import get_token_after_authentication
from utils import OAuth2PasswordBearerWithCookies

oauth_scheme = OAuth2PasswordBearerWithCookies(tokenUrl="/login/token")

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/logout")
def user_logged_out(db: Session = Depends(get_db), token: str = Depends(oauth_scheme)):
    user = get_token_after_authentication(db, token)
    if user is None:
        return responses.RedirectResponse("/?msg=You are not logged in!")
    else:
        # jwt_token = jwt.encode(user.email, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
        response.delete_cookie(key="access_token")
        return responses.RedirectResponse("/?msg=Successfully Logged out!")


@router.get("/login")
def login(request: Request, msg: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.post("/login")
async def login(request: Request, response: Response, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    errors = []
    if not email:
        errors.append("Please enter valid email!")
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": errors}
        )
    if not password or len(password) < 6:
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
            if Hash.verify_password(password, user.password):
                data = {"sub": email}
                jwt_token = jwt.encode(
                    data, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM
                )
                msg = "Login Successful!"
                response = templates.TemplateResponse(
                    "login.html", {"request": request, "errors": errors, "msg": msg}
                )
                response.set_cookie(
                    key="access_token", value=f"Bearer {jwt_token}", httponly=True
                )

                return response
            else:
                errors.append("Invalid password!")
                return templates.TemplateResponse(
                    "login.html", {"request": request, "errors": errors}
                )
    except:
        errors.append("something went wrong!")
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": errors}
        )
