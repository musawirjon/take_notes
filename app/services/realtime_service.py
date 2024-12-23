from app.services.websocket_manager import manager
from datetime import datetime

class RealtimeService:
    @staticmethod
    async def broadcast_note_update(meeting_id: str, note_data: dict):
        await manager.broadcast_to_room(meeting_id, {
            "type": "note_update",
            "data": note_data,
            "timestamp": datetime.utcnow().isoformat()
        })

    @staticmethod
    async def broadcast_transcription(meeting_id: str, transcription: str, speaker: str):
        await manager.broadcast_to_room(meeting_id, {
            "type": "transcription",
            "speaker": speaker,
            "content": transcription,
            "timestamp": datetime.utcnow().isoformat()
        })

    @staticmethod
    async def broadcast_summary_update(meeting_id: str, summary: str):
        await manager.broadcast_to_room(meeting_id, {
            "type": "summary_update",
            "content": summary,
            "timestamp": datetime.utcnow().isoformat()
        })

realtime = RealtimeService() 