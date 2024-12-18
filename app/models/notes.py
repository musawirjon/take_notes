from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(String(36), primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    summary = Column(Text, nullable=True)
    key_points = Column(Text, nullable=True)
    action_items = Column(Text, nullable=True)
    meeting_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(String(36), ForeignKey("users.id"))
    owner = relationship("User", back_populates="notes")