from sqlalchemy import Column, String, JSON, Integer, Boolean, DateTime  # Import DateTime here
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import Base, TimestampMixin

class ScheduledJob(Base, TimestampMixin):
    __tablename__ = "scheduled_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True)
    job_class = Column(String)
    cron_expression = Column(String)
    args = Column(JSON, default=list)
    kwargs = Column(JSON, default=dict)
    is_active = Column(Boolean, default=True)
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=True)
