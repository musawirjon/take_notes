from pydantic import BaseModel, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"

class JobBase(BaseModel):
    queue: str
    payload: Dict[str, Any]
    attempts: Optional[int] = 0
    status: JobStatus = JobStatus.PENDING

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    status: Optional[JobStatus] = None
    attempts: Optional[int] = None
    error: Optional[str] = None

class JobResponse(JobBase):
    id: UUID4
    reserved_at: Optional[datetime] = None
    available_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Scheduled Job Schemas
class ScheduledJobBase(BaseModel):
    name: str
    job_class: str
    cron_expression: str
    args: Optional[List[Any]] = []
    kwargs: Optional[Dict[str, Any]] = {}
    is_active: bool = True

class ScheduledJobCreate(ScheduledJobBase):
    pass

class ScheduledJobUpdate(BaseModel):
    name: Optional[str] = None
    cron_expression: Optional[str] = None
    args: Optional[List[Any]] = None
    kwargs: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class ScheduledJobResponse(ScheduledJobBase):
    id: UUID4
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Job Chain Schemas
class JobChainCreate(BaseModel):
    jobs: List[Dict[str, Any]]
    chain_name: Optional[str] = None

class JobChainResponse(BaseModel):
    id: UUID4
    chain_name: Optional[str]
    jobs: List[JobResponse]
    status: JobStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Job Progress Schema
class JobProgress(BaseModel):
    job_id: UUID4
    progress: int = 0
    total: int = 100
    status: JobStatus
    message: Optional[str] = None
    updated_at: datetime

    class Config:
        from_attributes = True 