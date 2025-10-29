from datetime import datetime
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


# Conversation Schemas
class ConversationCreateRequest(BaseModel):
    query: str


class ConversationCreateResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    response: str | None = None


class ConversationDetailResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[dict]
    documents: list[dict]


class ChangeTitleRequest(BaseModel):
    new_title: str


class AddMessageRequest(BaseModel):
    query: str


class AddMessageResponse(BaseModel):
    response: str
