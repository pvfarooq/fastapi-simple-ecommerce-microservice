from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator, validator


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    def email_min_length(cls, value):
        if len(value) < 5:
            raise ValueError("Email must be at least 5 characters long")
        return value

    @validator("password")
    def password_min_length(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value


class SignupRequest(BaseModel):
    first_name: str = None
    last_name: str = None
    email: EmailStr
    password: str

    @field_validator("email")
    def email_min_length(cls, value):
        if len(value) < 5:
            raise ValueError("Email must be at least 5 characters long")
        return value

    @validator("password")
    def password_min_length(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value


class Token(BaseModel):
    access_token: str
    token_type: str
    token_expire: datetime
