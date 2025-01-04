from sqlalchemy import Column, Integer, String

from core.db import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    order_id = Column(String(100), nullable=False, unique=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String(50), default="pending", nullable=False)
