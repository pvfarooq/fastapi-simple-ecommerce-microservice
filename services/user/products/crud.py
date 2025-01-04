from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from .models import Product
from .utils import get_mock_products


def get_products(session: Session, order_by: str = "-stock"):
    query = select(Product).order_by(text(order_by))
    products = session.execute(query)
    return products.scalars().all()


def get_product_by_id(session: Session, product_id: int):
    query = select(Product).filter(Product.id == product_id)
    product = session.execute(query).scalars().first()
    return product


def load_mock_products_to_db(session: Session):
    mock_products = get_mock_products()

    for data in mock_products:
        product = Product(**data)
        session.add(product)
    session.commit()
    session.close()
    print("Products loaded to DB")
