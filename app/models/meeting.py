from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .base import Base

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instance_id = Column(UUID(as_uuid=True), ForeignKey("instances.id"))
    title = Column(String, nullable=False)
    meeting_url = Column(String)
    platform = Column(String)  # zoom, teams, meet
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String, default="scheduled")
    summary = Column(Text)
    
    # Relationships
    instance = relationship("Instance", back_populates="meetings")
    participants = relationship("MeetingParticipant", back_populates="meeting")
    transcripts = relationship("Transcript", back_populates="meeting") 