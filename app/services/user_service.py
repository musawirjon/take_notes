from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
import app.crud.users as user
from app.schemas.user import UserCreate, UserUpdate
from app.auth.security import get_password_hash, verify_password
from fastapi import HTTPException

class UserService:
    @staticmethod
    async def create_user(db: Session, *, user_in: UserCreate) -> User:
        # Check if user exists
        if user.get_by_email(db, email=user_in.email):
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists"
            )
        
        # Hash password
        hashed_password = get_password_hash(user_in.password)
        instance_id = 1
        user_data = user_in.dict()
        user_data["hashed_password"] = hashed_password
        del user_data["password"]
        
        return user.create(db=db, obj_in=user_data)

    @staticmethod
    async def authenticate(db: Session, *, email: str, password: str) -> Optional[User]:
        user_obj = user.get_by_email(db, email=email)
        if not user_obj:
            return None
        if not verify_password(password, user_obj.hashed_password):
            return None
        return user_obj

    @staticmethod
    async def get_user_notes(db: Session, user_id: str, skip: int = 0, limit: int = 100):
        return user.get_notes(db=db, user_id=user_id, skip=skip, limit=limit) 