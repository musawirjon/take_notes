from fastapi import APIRouter, Depends, status
from app.controllers.auth_controller import AuthController
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    controller: AuthController = Depends()
):
    return await controller.register(user_data)

@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    controller: AuthController = Depends()
):
    return await controller.login(user_data) 