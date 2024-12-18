from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import models
from .routes import notes

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Notes API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes.router, prefix="/api/v1", tags=["notes"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Notes API"} 