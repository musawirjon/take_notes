from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.accounts import AccountCreate, AccountUpdate, AccountOut
from app.schemas.user import UserBase
from app.services.account_service import AccountService
from app.database import get_db
import uuid

router = APIRouter()

@router.post("/", response_model=AccountOut, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreate,
    db: Session = Depends(get_db)
):
    return await AccountService.create_account(db=db, account_in=account_data)

@router.get("/{account_id}", response_model=AccountOut)
async def get_account(account_id: uuid.UUID, db: Session = Depends(get_db)):
    # Fetch the account using the service
    account = await AccountService.get_account_by_id(db=db, account_id=account_id)
    return account

@router.put("/{account_id}", response_model=AccountOut)
async def update_account(
    account_id: uuid.UUID,
    account_data: AccountUpdate,
    db: Session = Depends(get_db)
):
    # Update account settings
    account = await AccountService.update_account_settings(db=db, account_id=account_id, settings=account_data.dict(exclude_unset=True))
    return account

@router.get("/{account_id}/users", response_model=UserBase)
async def get_account_users(
    account_id: uuid.UUID, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    # Fetch the users belonging to the account
    users = await AccountService.get_account_users(db=db, account_id=account_id, skip=skip, limit=limit)
    return users
