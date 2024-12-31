# app/models/meeting.py
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.models.base import Base

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    instance_id = Column(UUID(as_uuid=True), ForeignKey("instances.id"))

    # Relationships
    participants = relationship("MeetingParticipant", back_populates="meeting")
    instance = relationship("Instance", back_populates="meetings")
    transcripts = relationship("Transcript", back_populates="meeting")
