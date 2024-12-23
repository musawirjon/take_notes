from fastapi import HTTPException
import time
from app.services.cache_service import cache

class RateLimitService:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute

    async def check_rate_limit(self, user_id: str):
        current = int(time.time())
        key = f"rate_limit:{user_id}:{current // 60}"
        
        count = await cache.get(key) or 0
        if int(count) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )
        
        await cache.set(key, int(count) + 1, expire=60)

rate_limiter = RateLimitService() 