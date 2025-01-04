from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.db import get_session
from users import crud

from .schemas import LoginRequest, SignupRequest, Token

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
def register_user(request: SignupRequest, session=Depends(get_session)):
    user = crud.get_user_by_email(session=session, email=request.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.register_user(session=session, user_data=request)
    return {"message": "Registration successful"}


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> Token:
    login_data = LoginRequest(email=form_data.username, password=form_data.password)
    return crud.authenticate_user(login_data, session)
