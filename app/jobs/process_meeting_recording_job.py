from app.jobs.base_job import BaseJob
from app.services.background_service import process_recording_file

class ProcessMeetingRecordingJob(BaseJob):
    queue = "meetings"
    max_attempts = 2
    timeout = 7200  # 2 hours

    async def handle(self):
        meeting_id = self.kwargs.get("meeting_id")
        # Process the recording
        await process_recording_file(meeting_id) 