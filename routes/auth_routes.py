from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.auth_service import register_user, login_user
from models.schemas import (
    RegisterResponse,
    RegisterRequest,
    LoginRequest,
    LoginResponse,
)
from core.database import get_db


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    summary="Register a new user",
    description="Create a new user account with a username, email, and password.",
    response_description="Details of the registered user",
)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, request.username, request.email, request.password)
    return {"message": "User registered successfully", "user_id": user.id}


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="User login",
    description="Authenticate a user and return an access token.",
    response_description="Access token for the authenticated user",
)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, request.username, request.password)
