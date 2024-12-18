from fastapi import APIRouter, Depends, status
from app.controllers.user_controller import UserController
from app.schemas.user import UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    controller: UserController = Depends()
):
    return await controller.get_current_user_info()

@router.put("/me", response_model=UserResponse)
async def update_user_info(
    user_data: UserUpdate,
    controller: UserController = Depends()
):
    return await controller.update_user_info(user_data)

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_account(
    controller: UserController = Depends()
):
    return await controller.delete_user_account() 