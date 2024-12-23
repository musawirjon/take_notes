from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.job import Job
from app.models.scheduled_job import ScheduledJob
from app.schemas.jobs import (
    JobStatus,
    ScheduledJobCreate,
    ScheduledJobUpdate,
    JobResponse,
    ScheduledJobResponse
)
from app.services.job_scheduler import scheduler

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/", response_model=List[JobResponse])
async def get_jobs(
    skip: int = 0,
    limit: int = 100,
    status: JobStatus = None,
    db: Session = Depends(get_db)
):
    """Get all jobs with optional filtering"""
    query = db.query(Job)
    if status:
        query = query.filter(Job.status == status)
    return query.offset(skip).limit(limit).all()

@router.get("/scheduled", response_model=List[ScheduledJobResponse])
async def get_scheduled_jobs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all scheduled jobs"""
    return db.query(ScheduledJob).offset(skip).limit(limit).all()

@router.post("/scheduled", response_model=ScheduledJobResponse)
async def create_scheduled_job(
    job_in: ScheduledJobCreate,
    db: Session = Depends(get_db)
):
    """Create a new scheduled job"""
    return await scheduler.schedule_job(
        name=job_in.name,
        job_class=job_in.job_class,
        cron_expression=job_in.cron_expression,
        args=job_in.args,
        kwargs=job_in.kwargs
    )

@router.delete("/jobs/{job_id}")
async def delete_job(job_id: str, db: Session = Depends(get_db)):
    """Delete a job"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted"} 