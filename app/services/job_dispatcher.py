from sqlalchemy.orm import Session
from typing import Optional
from app.models.job import Job
from app.schemas.jobs import JobCreate, JobUpdate, JobStatus, JobProgress
from datetime import datetime

class JobDispatcher:
    @staticmethod
    async def dispatch(db: Session, job_data: JobCreate) -> Job:
        db_job = Job(
            queue=job_data.queue,
            payload=job_data.payload,
            status=JobStatus.PENDING
        )
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job

    @staticmethod
    async def update_job(db: Session, job_id: str, job_update: JobUpdate) -> Optional[Job]:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return None

        update_data = job_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(job, field, value)

        if job_update.status == JobStatus.FAILED:
            job.failed_at = datetime.utcnow()

        db.commit()
        db.refresh(job)
        return job

    @staticmethod
    async def get_progress(db: Session, job_id: str) -> Optional[JobProgress]:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return None

        # Extract progress from job payload if available
        progress = job.payload.get('progress', 0)
        total = job.payload.get('total', 100)

        return JobProgress(
            job_id=job.id,
            progress=progress,
            total=total,
            status=job.status,
            message=job.error,
            updated_at=job.updated_at
        )

job_dispatcher = JobDispatcher() 