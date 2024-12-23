import asyncio
import typer
from app.db.session import SessionLocal
from app.services.job_worker import JobWorker

app = typer.Typer()

@app.command()
def run_worker(queue: str = "default"):
    """Run job worker for specified queue"""
    db = SessionLocal()
    worker = JobWorker(db)
    
    while True:
        asyncio.run(worker.process_jobs(queue))
        typer.echo(f"Processed jobs in queue: {queue}")
        asyncio.sleep(10)  # Wait 10 seconds before next check

if __name__ == "__main__":
    app() 