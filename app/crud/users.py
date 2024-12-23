from sqlalchemy.orm import Session
from app.models.user import User  # Assuming User is an SQLAlchemy model
from app.schemas.user import UserCreate, UserUpdate
from app.auth.security import get_password_hash, verify_password
from app.models.notes import Note  # Assuming Note is a related model for user notes
from typing import Optional

# CRUD operations for the user

def create(db: Session, obj_in: dict) -> User:
    """
    Create a new user.
    """
    db_user = User(**obj_in)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by email.
    """
    return db.query(User).filter(User.email == email).first()


def update(db: Session, user_id: int, obj_in: UserUpdate) -> User:
    """
    Update an existing user's details.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def delete(db: Session, user_id: int) -> Optional[User]:
    """
    Delete a user by ID.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None


def get_notes(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """
    Get all notes for a given user.
    """
    return db.query(Note).filter(Note.user_id == user_id).offset(skip).limit(limit).all()
