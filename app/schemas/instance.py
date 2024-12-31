from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

# Pydantic schemas for Instance
class InstanceBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    ai_settings: Optional[str] = "{}"  # AI-specific settings in JSON format

class InstanceCreate(InstanceBase):
    pass  # Inherits all fields for creating an instance

class InstanceUpdate(InstanceBase):
    # Fields for updating an instance
    name: Optional[str]
    description: Optional[str]
    is_active: Optional[bool]
    ai_settings: Optional[str]

class InstanceOut(InstanceBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # This tells Pydantic to treat SQLAlchemy models as dicts

