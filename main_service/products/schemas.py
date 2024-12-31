from typing import List

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    description: str


class ProductList(BaseModel):
    products: List[Product]
