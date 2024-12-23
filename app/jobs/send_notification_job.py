from app.jobs.base_job import BaseJob
from app.services.notification_service import notification

class SendNotificationJob(BaseJob):
    queue = "notifications"
    max_attempts = 3
    timeout = 300  # 5 minutes

    async def handle(self):
        await notification.send_meeting_summary(
            recipients=self.kwargs.get("recipients"),
            meeting_summary=self.kwargs.get("summary"),
            meeting_title=self.kwargs.get("title")
        ) 