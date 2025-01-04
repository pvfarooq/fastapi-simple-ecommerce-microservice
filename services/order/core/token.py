import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer

from .config import Audiences, settings

auth_scheme = HTTPBearer()


def verify_token(request: Request, token: str = Depends(auth_scheme)):
    """Verify JWT token and extract user payload.

    This function validates a JWT token from the request and sets the decoded payload
    in request.state.user if valid. It checks the token signature, expiration,
    issuer and audience claims.
    """
    try:
        payload = jwt.decode(
            token.credentials,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_aud": True},
            audience=Audiences.ORDER_SERVICE,
            issuer=settings.ISSUER,
        )
        request.state.user = payload["sub"]
        request.state.bearer_token = token.credentials
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidIssuerError:
        raise HTTPException(status_code=401, detail="Invalid issuer")
    except jwt.InvalidAudienceError:
        raise HTTPException(status_code=401, detail="Invalid audience")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
