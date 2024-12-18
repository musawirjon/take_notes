from datetime import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.schemas.auth import UserCreate, UserLogin, Token
from backend.app.services import user_service
from backend.app.auth.security import verify_password
from backend.app.auth.jwt import create_access_token, create_refresh_token

class AuthController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.user_service = user_service.UserService(db)

    async def register(self, user_data: UserCreate):
        if self.user_service.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        return self.user_service.create(user_data)

    async def login(self, user_data: UserLogin):
        user = self.user_service.get_by_email(user_data.email)
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