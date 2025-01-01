from core.exceptions import AlreadyExistsException, UnauthorizedException
from core.pwd_hasher import get_password_hash, verify_password
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import User
from .schemas import Token
from .token import create_access_token


def get_user_by_email(email: str, session: Session) -> User:
    query = select(User).where(User.email == email)
    user = session.execute(query)
    user = user.scalar_one_or_none()
    return user


def get_user_by_id(user_id: int, session: Session) -> User:
    query = select(User).where(User.id == user_id)
    user = session.execute(query)
    user = user.scalar_one_or_none()
    return user


def register_user(user_data: dict, session: Session) -> User:
    user = get_user_by_email(user_data.email, session)
    if user is not None:
        raise AlreadyExistsException(detail="Email already registered")

    password = get_password_hash(user_data.password)
    user = User(**user_data.dict(exclude={"password"}), password=password)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(login_data: dict, session: Session) -> Token:
    user = get_user_by_email(login_data.email, session)
    if not user or not verify_password(login_data.password, user.password):
        raise UnauthorizedException(detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": str(user.id)})
    return access_token
