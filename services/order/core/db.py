from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings


def get_db_url():
    return settings.SQLALCHEMY_DATABASE_URI


Base = declarative_base()

engine = create_engine(get_db_url())

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = session_local()
    try:
        yield session
    finally:
        session.close()
