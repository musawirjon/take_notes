from abc import ABC, abstractmethod
from typing import Any, Dict
from app.schemas.jobs import JobCreate, JobStatus
from sqlalchemy.orm import Session
from datetime import datetime
from app.jobs.retry_strategies import RetryStrategy, ExponentialBackoff
from app.services.job_dispatcher import job_dispatcher
from app.models.job import Job


class BaseJob(ABC):
    queue = "default"
    max_attempts = 3
    timeout = 3600  # 1 hour
    retry_strategy: RetryStrategy = ExponentialBackoff()

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @abstractmethod
    async def handle(self) -> Any:
        """Execute the job"""
        pass

    def to_job_create(self) -> JobCreate:
        """Convert job to JobCreate schema"""
        return JobCreate(
            queue=self.queue,
            payload={
                "job_class": self.__class__.__name__,
                "args": self.args,
                "kwargs": self.kwargs,
                "max_attempts": self.max_attempts,
                "timeout": self.timeout
            }
        )

    @classmethod
    async def dispatch(cls, db: Session, *args, **kwargs) -> Job:
        """Create and dispatch a new job"""
        job = cls(*args, **kwargs)
        job_create = job.to_job_create()
        return await job_dispatcher.dispatch(db=db, job_data=job_create)

    def get_next_retry_time(self, attempts: int) -> datetime:
        return self.retry_strategy.next_retry_time(attempts)