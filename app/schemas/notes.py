from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NoteBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    key_points: Optional[str] = None
    action_items: Optional[str] = None
    meeting_date: Optional[datetime] = None

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: str
    created_at: datetime
    updated_at: datetime
    user_id: str

    class Config:
        from_attributes = True