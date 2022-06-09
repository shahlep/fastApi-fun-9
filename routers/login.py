from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login/token")

router = APIRouter()


@router.post("/login/token", tags=["Login"])
def get_token_after_authentication():
    pass
