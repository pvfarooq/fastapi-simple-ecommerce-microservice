from core.db import Base
from sqlalchemy import Column, Integer, String


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(String(128))
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
