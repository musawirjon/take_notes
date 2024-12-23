from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional, List

class MeetingBase(BaseModel):
    title: str
    meeting_url: str
    platform: str
    start_time: datetime
    end_time: Optional[datetime] = None

class MeetingCreate(MeetingBase):
    instance_id: UUID4

class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    summary: Optional[str] = None

class MeetingInDB(MeetingBase):
    id: UUID4
    instance_id: UUID4
    status: str
    summary: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True 