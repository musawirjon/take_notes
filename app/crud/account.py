from sqlalchemy.orm import Session
from app.models.account import Account
from app.models.user import User
import uuid

class AccountCRUD:
    def create(db: Session, obj_in: dict) -> Account:
        db_account = Account(**obj_in)
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return db_account

    def get_by_domain(db: Session, domain: str) -> Account:
        return db.query(Account).filter(Account.domain == domain).first()

    def get_by_id(db: Session, account_id: uuid.UUID) -> Account:
        return db.query(Account).filter(Account.id == account_id).first()

    def get_users(db: Session, account_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list:
        return db.query(User).filter(User.account_id == account_id).offset(skip).limit(limit).all()
