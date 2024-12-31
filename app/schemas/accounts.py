from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

# Schema for Account creation
class AccountCreate(BaseModel):
    name: str
    domain: str

# Schema for Account update (partial updates allowed)
class AccountUpdate(BaseModel):
    name: Optional[str]
    domain: Optional[str]
    settings: Optional[dict]  # JSON object for settings

# Schema for Account output (what we return in API responses)
class AccountOut(AccountCreate):
    id: uuid.UUID
    settings: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Tells Pydantic to treat SQLAlchemy models as dicts
