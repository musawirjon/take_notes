from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

# Base User Schema (shared properties)
class UserBase(BaseModel):
    email: EmailStr
    username: str  # Not optional, required field
    full_name: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False

# Schema for creating a user
class UserCreate(UserBase):
    password: str

# Schema for updating a user
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None

# Schema for reading user data
class User(UserBase):
    id: UUID
    instance_id: Optional[UUID] = None
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schema for user with token (login response)
class UserWithToken(User):
    access_token: str
    token_type: str = "bearer"

# Schema for user response
class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool
    is_verified: bool
    instance_id: Optional[UUID] = None
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        orm_mode = True  # Enables ORM mode
        arbitrary_types_allowed = True  # Allows custom types
        from_attributes = True  # Allows model to read data from ORM objects
