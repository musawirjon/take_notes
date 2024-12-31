# app/models/meeting_participant.py
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.models.base import Base

class MeetingParticipant(Base):
    __tablename__ = "meeting_participants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id"))
    role = Column(String)  # e.g., "host", "participant", etc.

    # Relationships
    user = relationship("User", back_populates="meeting_participants")
    meeting = relationship("Meeting", back_populates="participants")
    