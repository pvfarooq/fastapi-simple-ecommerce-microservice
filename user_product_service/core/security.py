import jwt
from core.db import session_local
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from users import crud

from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        token_data = {"user_id": user_id}
        with session_local() as session:
            user = crud.get_user_by_id(token_data["user_id"], session)
            if user is None:
                raise HTTPException(status_code=404, detail="Invalid user")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return token_data
