import os


class Audiences:
    ORDER_SERVICE = "https://orders.myapp.com"
    PRODUCT_SERVICE = "https://products.myapp.com"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = "HS256"
    ISSUER = "https://www.identity.myapp.com"

    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Config()
