from core.db import get_session
from fastapi import APIRouter, Depends
from products import crud
from sqlalchemy.orm import Session

from .schemas import ProductList

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
def list_products(session: Session = Depends(get_session)) -> ProductList:
    products = crud.get_products(session)
    print(products)
    return ProductList(products=products)


@router.post("/load-mock-data")
def load_products(session: Session = Depends(get_session)):
    crud.load_mock_products_to_db(session)
    return {"message": "Products loaded to DB"}
