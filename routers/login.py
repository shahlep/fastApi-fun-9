from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from hashing import Hash
from jose import jwt
from config.settings import Settings

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

router = APIRouter()


@router.post("/login/token", tags=["Login"])
def get_token_after_authentication(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username!"
        )

    if not Hash.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password!"
        )

    data = {"sub":form_data.username}
    jwt_token = jwt.encode(data,Settings.SECURITY_KEY,algorithm=Settings.ALGORITHM)
    return {"access_token":jwt_token,"token_type":"bearer"}

