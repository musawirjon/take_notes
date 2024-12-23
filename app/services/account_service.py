from sqlalchemy.orm import Session
from app.crud.account import account
from app.schemas.accounts import AccountCreate, AccountUpdate
from typing import List

class AccountService:
    @staticmethod
    async def create_account(db: Session, *, account_in: AccountCreate):
        # Validate domain uniqueness
        if account.get_by_domain(db, domain=account_in.domain):
            raise HTTPException(
                status_code=400,
                detail="Account with this domain already exists"
            )
        
        # Set up account settings
        account_data = account_in.dict()
        account_data["settings"] = {
            "max_users": 10,
            "max_storage": 5_000_000_000,  # 5GB
            "features": ["basic", "notes", "meetings"]
        }
        
        return account.create(db=db, obj_in=account_data)

    @staticmethod
    async def get_account_users(
        db: Session,
        account_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        return account.get_users(db=db, account_id=account_id, skip=skip, limit=limit)

    @staticmethod
    async def update_account_settings(
        db: Session,
        account_id: str,
        settings: dict
    ):
        return account.update_settings(db=db, account_id=account_id, settings=settings) 