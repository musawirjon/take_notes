from app.jobs.base_job import BaseJob
from app.services.background_service import BackgroundService

class ProcessMeetingJob(BaseJob):
    queue = "meetings"
    max_attempts = 2
    timeout = 7200  # 2 hours

    async def handle(self):
        meeting_id = self.kwargs.get("meeting_id")
        meeting_service = MeetingService()
        await BackgroundService.process_meeting_recording(meeting_id) 