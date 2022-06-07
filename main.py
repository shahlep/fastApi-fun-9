import uvicorn
from fastapi import FastAPI
from config.settings import settings
from database import engine
from models import Base
from routers import user


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    openapi_url=settings.api_json_version,
    version=settings.app_version,
    openapi_tags=settings.tags,
)

app.include_router(user.router)


@app.get("/product", tags=["Product"])
def get_product():
    return {"message": "Hello Product"}


if __name__ == "__main__":
    uvicorn.run(app)
