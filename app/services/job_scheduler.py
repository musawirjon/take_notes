from croniter import croniter
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.scheduled_job import ScheduledJob
from app.services.job_dispatcher import job_dispatcher
import importlib

class JobScheduler:
    def __init__(self, db: Session):
        self.db = db

    async def schedule_job(
        self,
        name: str,
        job_class: str,
        cron_expression: str,
        args: list = None,
        kwargs: dict = None
    ):
        """Schedule a new recurring job"""
        next_run = croniter(cron_expression, datetime.utcnow()).get_next(datetime)
        
        scheduled_job = ScheduledJob(
            name=name,
            job_class=job_class,
            cron_expression=cron_expression,
            args=args or [],
            kwargs=kwargs or {},
            next_run=next_run
        )
        
        self.db.add(scheduled_job)
        self.db.commit()
        return scheduled_job

    async def process_scheduled_jobs(self):
        """Process all due scheduled jobs"""
        now = datetime.utcnow()
        due_jobs = self.db.query(ScheduledJob).filter(
            ScheduledJob.is_active == True,
            ScheduledJob.next_run <= now
        ).all()

        for job in due_jobs:
            # Dispatch the job
            job_class = self._import_job_class(job.job_class)
            await job_dispatcher.dispatch(
                self.db,
                job_class,
                *job.args,
                **job.kwargs
            )

            # Update next run time
            job.last_run = now
            job.next_run = croniter(job.cron_expression, now).get_next(datetime)

        self.db.commit()

    def _import_job_class(self, class_name: str):
        module = importlib.import_module(f"app.jobs.{class_name.lower()}")
        return getattr(module, class_name)

scheduler = JobScheduler(db=SessionLocal()) 