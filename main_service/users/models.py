from core.db import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
