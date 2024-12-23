from typing import Any, Optional
import redis
import os

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=0,
            decode_responses=True
        )

    async def get(self, key: str) -> Optional[Any]:
        return self.redis_client.get(key)

    async def set(self, key: str, value: Any, expire: int = 3600):
        self.redis_client.set(key, value, ex=expire)

    async def delete(self, key: str):
        self.redis_client.delete(key)

    async def clear_all(self):
        self.redis_client.flushall()

cache = CacheService()