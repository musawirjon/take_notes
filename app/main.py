from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
import importlib
import os
from app import models
from app.database import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Notes API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dynamically import all route modules from the routes directory
routes_dir = os.path.join(os.path.dirname(__file__), "routers")
for filename in os.listdir(routes_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]  # Remove .py extension
        module = importlib.import_module(f"app.routers.{module_name}")
        if hasattr(module, "router"):
            app.include_router(module.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Notes API"} 