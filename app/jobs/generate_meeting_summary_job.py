from app.jobs.base_job import BaseJob

class GenerateMeetingSummaryJob(BaseJob):
    queue = "summaries"
    max_attempts = 3
    timeout = 1800  # 30 minutes

    async def handle(self):
        meeting_id = self.kwargs.get("meeting_id")
        # Generate meeting summary
        await self.generate_and_save_summary(meeting_id) 
    
    @staticmethod
    async def generate_and_save_summary(meeting_id: str):
        # Summary generation logic here
        pass
