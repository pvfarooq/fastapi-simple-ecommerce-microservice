from datetime import datetime, timedelta

import jwt
from core.config import settings

from .schemas import Token


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> Token:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(
            seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
        )
    to_encode.update({"exp": expire})
    access_token = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return Token(access_token=access_token, token_type="bearer", token_expire=expire)
