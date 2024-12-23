import pytest
from app.schemas.jobs import JobStatus
from app.services.job_dispatcher import job_dispatcher
from app.services.job_worker import JobWorker

@pytest.mark.asyncio
async def test_job_lifecycle(auth_client, db):
    # Create job
    response = auth_client.post(
        "/api/jobs/",
        json={
            "queue": "test",
            "payload": {
                "job_class": "TestJob",
                "args": [],
                "kwargs": {"test": "data"}
            }
        }
    )
    assert response.status_code == 200
    job_id = response.json()["id"]

    # Check status
    status_response = auth_client.get(f"/api/jobs/{job_id}")
    assert status_response.status_code == 200
    assert status_response.json()["status"] == JobStatus.PENDING

    # Process job
    worker = JobWorker(db)
    await worker.process_jobs("test")

    # Verify completion
    final_status = auth_client.get(f"/api/jobs/{job_id}")
    assert final_status.json()["status"] == JobStatus.COMPLETED

@pytest.mark.asyncio
async def test_job_failure_handling(auth_client, db):
    # Create job that will fail
    response = auth_client.post(
        "/api/jobs/",
        json={
            "queue": "test",
            "payload": {
                "job_class": "FailingJob",
                "args": [],
                "kwargs": {}
            }
        }
    )
    job_id = response.json()["id"]

    # Process job
    worker = JobWorker(db)
    await worker.process_jobs("test")

    # Check failure status
    status = auth_client.get(f"/api/jobs/{job_id}")
    assert status.json()["status"] == JobStatus.FAILED
    assert status.json()["error"] is not None

@pytest.mark.asyncio
async def test_job_retry_mechanism(auth_client, db):
    # Create job with retry
    response = auth_client.post(
        "/api/jobs/",
        json={
            "queue": "test",
            "payload": {
                "job_class": "RetryableJob",
                "args": [],
                "kwargs": {},
                "max_attempts": 3
            }
        }
    )
    job_id = response.json()["id"]

    # Process and check retries
    worker = JobWorker(db)
    await worker.process_jobs("test")

    status = auth_client.get(f"/api/jobs/{job_id}")
    assert status.json()["attempts"] > 0 