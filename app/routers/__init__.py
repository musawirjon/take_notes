from fastapi import APIRouter
from app.routers import users, notes, meetings, auth

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(meetings.router, prefix="/meetings", tags=["meetings"]) 