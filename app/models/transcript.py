from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime  # Add this import to fix the issue
from .base import Base

class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id"), nullable=False)
    content = Column(Text, nullable=False)  # The actual transcript content
    status = Column(String, default="pending")  # e.g., "pending", "completed", "reviewed"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationship to Meeting
    meeting = relationship("Meeting", back_populates="transcripts")  # One-to-many with Meeting
