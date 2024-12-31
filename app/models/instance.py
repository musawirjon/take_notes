from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .base import Base

class Instance(Base):
    __tablename__ = "instances"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)  # Instance Name (e.g. "Marketing", "Engineering")
    account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.id'))  # Foreign Key to Account
    description = Column(String, nullable=True)  # Optional Description
    is_active = Column(Boolean, default=True)  # Whether the instance is active or archived
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    account = relationship("Account", back_populates="instances")  # One-to-many with Account
    users = relationship("User", back_populates="instance")
    meetings = relationship("Meeting", back_populates="instance")

    # Optional: AI-specific settings for this instance
    ai_settings = Column(String, default="{}")  # Stores AI settings in JSON

    # Optional: Usage metrics for instance (can be extended)
    note_quota = Column(Integer, default=1000)  # Max number of notes
    storage_used = Column(Integer, default=0)  # Storage used by notes (KB, MB, etc.)
