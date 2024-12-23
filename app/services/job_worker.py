from sqlalchemy.orm import Session
import importlib
from datetime import datetime
import logging
from app.models.job import Job
from app.schemas.jobs import JobStatus, JobUpdate
from app.core.config import settings

logger = logging.getLogger(__name__)

class JobWorker:
    def __init__(self, db: Session):
        self.db = db

    async def process_jobs(self, queue: str = "default"):
        """Process pending jobs in the specified queue"""
        jobs = self.db.query(Job).filter(
            Job.queue == queue,
            Job.status == JobStatus.PENDING,
            Job.available_at <= datetime.utcnow(),
            Job.reserved_at.is_(None)
        ).all()

        for job in jobs:
            await self.process_job(job)

    async def process_job(self, job: Job):
        """Process a single job"""
        try:
            # Mark job as processing
            await job_dispatcher.update_job(
                self.db,
                job.id,
                JobUpdate(status=JobStatus.PROCESSING)
            )

            # Import and instantiate job class
            job_data = job.payload
            job_class = self._import_job_class(job_data["job_class"])
            job_instance = job_class(*job_data.get("args", []), **job_data.get("kwargs", {}))

            # Execute job
            await job_instance.handle()

            # Mark job as completed
            await job_dispatcher.update_job(
                self.db,
                job.id,
                JobUpdate(status=JobStatus.COMPLETED)
            )

        except Exception as e:
            logger.error(f"Error processing job {job.id}: {str(e)}")
            await job_dispatcher.update_job(
                self.db,
                job.id,
                JobUpdate(
                    status=JobStatus.FAILED,
                    error=str(e)
                )
            )

    def _import_job_class(self, class_name: str):
        """Dynamically import job class"""
        module = importlib.import_module(f"app.jobs.{class_name.lower()}")
        return getattr(module, class_name) 