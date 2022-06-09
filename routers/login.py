from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import APIRouter

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login/token")

router = APIRouter()


@router.post("/login/token", tags=["Login"])
def get_token_after_authentication(form_data:OAuth2PasswordRequestForm):
    pass
