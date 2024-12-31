from sqlalchemy.orm import Session
from app.crud.account import AccountCRUD
from app.schemas.accounts import AccountCreate, AccountUpdate
from app.models.user import User
from typing import List
from fastapi import HTTPException, status
import uuid

class AccountService:
    @staticmethod
    async def create_account(db: Session, *, account_in: AccountCreate):
        # Check if the domain is already used
        if account.get_by_domain(db, domain=account_in.domain):
            raise HTTPException(
                status_code=400,
                detail="Account with this domain already exists"
            )
        
        # Prepare account data including default settings
        account_data = account_in.dict()
        account_data["settings"] = {
            "max_users": 10,
            "max_storage": 5_000_000_000,  # 5GB in bytes
            "features": ["basic", "notes", "meetings"]
        }

        return await account.create(db=db, obj_in=account_data)

    @staticmethod
    async def get_account_by_id(db: Session, account_id: uuid.UUID):
        account = account.get_by_id(db, account_id=account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        return account

    @staticmethod
    async def update_account_settings(db: Session, account_id: uuid.UUID, settings: dict):
        account_data = account.get_by_id(db, account_id=account_id)
        if not account_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        # Update settings
        account_data.settings.update(settings)
        db.commit()
        db.refresh(account_data)
        return account_data

    @staticmethod
    async def get_account_users(db: Session, account_id: uuid.UUID, skip: int = 0, limit: int = 100) -> User:
        return account.get_users(db=db, account_id=account_id, skip=skip, limit=limit)
