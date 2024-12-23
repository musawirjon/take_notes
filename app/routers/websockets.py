from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.services.websocket_manager import manager
from app.auth.dependencies import get_current_user_ws
from typing import Optional

router = APIRouter()

@router.websocket("/ws/meeting/{meeting_id}")
async def meeting_websocket(
    websocket: WebSocket,
    meeting_id: str,
    token: Optional[str] = None
):
    # Authenticate user
    user = await get_current_user_ws(token)
    if not user:
        await websocket.close(code=4001)
        return

    try:
        await manager.connect(websocket, meeting_id)
        
        # Listen for messages
        while True:
            data = await websocket.receive_json()
            # Handle different types of messages
            if data["type"] == "note":
                await manager.broadcast_to_room(meeting_id, {
                    "type": "note",
                    "user": user.full_name,
                    "content": data["content"],
                    "timestamp": data["timestamp"]
                })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, meeting_id) 