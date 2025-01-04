import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer

from core.db import session_local
from users import crud

from .config import Audiences, settings

auth_scheme = HTTPBearer()


def get_current_user(request: Request, token: str = Depends(auth_scheme)):
    try:
        payload = jwt.decode(
            token.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            audience=[Audiences.PRODUCT_SERVICE, Audiences.ORDER_SERVICE],
            issuer=settings.ISSUER,
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        with session_local() as session:
            user = crud.get_user_by_id(user_id, session)
            if user is None:
                raise HTTPException(status_code=404, detail="Invalid user")
        request.state.user = user
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return user_id
