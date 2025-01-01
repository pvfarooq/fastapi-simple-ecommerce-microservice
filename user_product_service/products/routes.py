from core.db import get_session
from core.security import get_current_user
from fastapi import APIRouter, Depends
from products import crud
from sqlalchemy.orm import Session

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
def list_products(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    products = crud.get_products(session)
    return products


@router.get("/{product_id}")
def get_product(
    product_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return crud.get_product_by_id(session, product_id)


# @router.post("/load-mock-data")
# def load_products(session: Session = Depends(get_session)):
#     crud.load_mock_products_to_db(session)
#     return {"message": "Products loaded to DB"}
