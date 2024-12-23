from prometheus_client import Counter, Histogram, Gauge
from datetime import datetime

class JobMetrics:
    def __init__(self):
        self.job_duration = Histogram(
            'job_duration_seconds',
            'Time spent processing jobs',
            ['job_type', 'queue']
        )
        self.job_failures = Counter(
            'job_failures_total',
            'Number of job failures',
            ['job_type', 'queue']
        )
        self.queued_jobs = Gauge(
            'queued_jobs',
            'Number of jobs in queue',
            ['queue']
        )

    def record_job_duration(self, job_type: str, queue: str, duration: float):
        self.job_duration.labels(job_type=job_type, queue=queue).observe(duration)

    def record_job_failure(self, job_type: str, queue: str):
        self.job_failures.labels(job_type=job_type, queue=queue).inc()

    def update_queue_size(self, queue: str, size: int):
        self.queued_jobs.labels(queue=queue).set(size)

metrics = JobMetrics() 