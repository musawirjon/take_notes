from sqlalchemy import Column, String, JSON, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from .base import Base, TimestampMixin

class Job(Base, TimestampMixin):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    queue = Column(String, index=True)
    payload = Column(JSON)
    attempts = Column(Integer, default=0)
    reserved_at = Column(DateTime, nullable=True)
    available_at = Column(DateTime, default=datetime.utcnow)
    failed_at = Column(DateTime, nullable=True)
    error = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, processing, completed, failed 