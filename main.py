import uvicorn
from fastapi import FastAPI, Depends
from config.settings import settings
from database import engine, get_db
from models import Base, User
from schemas import UserCreate
from sqlalchemy.orm import Session
from hashing import Hash

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    openapi_url=settings.api_json_version,
    version=settings.app_version,
    openapi_tags=settings.tags,
)


@app.get("/user", tags=["User"])
def get_user():
    return {"message": "Hello User"}


@app.get("/product", tags=["Product"])
def get_product():
    return {"message": "Hello Product"}


@app.post("/create_user", tags=["User"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = User(email=user.email, password=Hash.get_hash_password(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


if __name__ == "__main__":
    uvicorn.run(app)
