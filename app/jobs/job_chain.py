from typing import List, Type
from app.jobs.base_job import BaseJob
from sqlalchemy.orm import Session

class JobChain:
    def __init__(self, initial_job: Type[BaseJob], *args, **kwargs):
        self.jobs = [(initial_job, args, kwargs)]
        self.then_jobs = []

    def then(self, job: Type[BaseJob], *args, **kwargs):
        """Add a job to be executed after the previous job completes"""
        self.then_jobs.append((job, args, kwargs))
        return self

    async def dispatch(self, db: Session):
        """Dispatch the entire job chain"""
        previous_job = None
        for job_class, args, kwargs in [*self.jobs, *self.then_jobs]:
            if previous_job:
                kwargs['previous_job_id'] = previous_job.id
            current_job = await job_class.dispatch(db, *args, **kwargs)
            previous_job = current_job
        return previous_job 