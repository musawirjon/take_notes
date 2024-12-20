from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserUpdate
from app.models.user import User
from app.services import user_service
from app.auth.dependencies import get_current_user

class UserController:
    def __init__(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        self.db = db
        self.current_user = current_user
        self.user_service = user_service.UserService(db)

    async def get_current_user_info(self):
        return self.current_user

    async def update_user_info(self, user_data: UserUpdate):
        return self.user_service.update(self.current_user, user_data)

    async def delete_user_account(self):
        return self.user_service.delete(self.current_user) 