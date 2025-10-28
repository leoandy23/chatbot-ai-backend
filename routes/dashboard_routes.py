# routes/dashboard.py
from typing import Annotated
from fastapi import APIRouter, Depends
from models.models import User
from dependencies.auth_dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("")
async def get_dashboard(current_user: Annotated[User, Depends(get_current_user)]):
    return {"message": f"Welcome to the dashboard, {current_user.email}!"}
