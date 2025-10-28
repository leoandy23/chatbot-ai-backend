from uuid import UUID
from pydantic import BaseModel


# Auth Schemas


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class RegisterResponse(BaseModel):
    message: str
    user_id: UUID
