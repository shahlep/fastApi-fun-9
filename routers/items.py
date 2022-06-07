from fastapi import APIRouter

router = APIRouter()


@router.get("/product", tags=["Product"])
def get_product():
    return {"message": "Hello Product"}
