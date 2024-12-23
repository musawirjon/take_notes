from typing import List, Optional
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings

class NotificationService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_TLS=True,
            MAIL_SSL=False,
            USE_CREDENTIALS=True
        )
        self.fastmail = FastMail(self.conf)

    async def send_meeting_summary(
        self,
        recipients: List[str],
        meeting_summary: str,
        meeting_title: str
    ):
        message = MessageSchema(
            subject=f"Meeting Summary: {meeting_title}",
            recipients=recipients,
            body=meeting_summary,
            subtype="html"
        )
        await self.fastmail.send_message(message)

    async def send_note_shared(
        self,
        recipient: str,
        note_title: str,
        shared_by: str
    ):
        message = MessageSchema(
            subject=f"Note Shared: {note_title}",
            recipients=[recipient],
            body=f"{shared_by} has shared a note with you: {note_title}",
            subtype="html"
        )
        await self.fastmail.send_message(message)

notification = NotificationService() 