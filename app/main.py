from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.error_handler import error_handler_middleware
from app.services.rate_limit_service import rate_limiter
from app.auth.dependencies import get_current_user
from app.core.config import settings
from app.routers import api_router

app = FastAPI(title=settings.PROJECT_NAME)

# Middleware
app.middleware("http")(error_handler_middleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting dependency
async def check_rate_limit(current_user = Depends(get_current_user)):
    await rate_limiter.check_rate_limit(str(current_user.id))
    return current_user

# Include routers with rate limiting
app.include_router(
    api_router,
    dependencies=[Depends(check_rate_limit)]
)

@app.on_event("startup")
async def startup_event():
    # Initialize services
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Cleanup services
    pass 