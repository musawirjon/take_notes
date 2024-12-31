# app/models/user.py
from datetime import datetime
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Foreign Keys
    instance_id = Column(UUID(as_uuid=True), ForeignKey("instances.id"))

    # Relationships
    instance = relationship("Instance", back_populates="users")
    notes = relationship("Note", back_populates="owner")
    meeting_participants = relationship("MeetingParticipant", back_populates="user")

