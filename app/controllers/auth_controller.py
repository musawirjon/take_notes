from datetime import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import UserCreate, UserLogin, Token
from app.services.user_service import UserService
from app.auth.security import verify_password
from app.auth.jwt import create_access_token, create_refresh_token

class AuthController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def register(self, user_data: UserCreate):
        return UserService.create_user(self.db, user_in=user_data)

    async def login(self, user_data: UserLogin):
        user = self.UserService.get_by_email(user_data.email)
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Update last login
        user.last_login = datetime.utcnow()
        self.db.commit()

        return {
            "access_token": create_access_token({"sub": user.id}),
            "refresh_token": create_refresh_token({"sub": user.id}),
            "token_type": "bearer"
        } 