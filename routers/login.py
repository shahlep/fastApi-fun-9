from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login/token")


router = APIRouter()

