"""Redis 캐시를 제공하는 모듈입니다."""

import json
from typing import Any, Optional
from redis import Redis

from .base import BaseCache
from ..core.settings import get_settings


class RedisCache(BaseCache):
    """Redis 캐시 클래스입니다."""

    def __init__(self):
        """Redis 캐시를 초기화합니다."""
        settings = get_settings()
        self.redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def get(self, key: str) -> Optional[Any]:
        """캐시에서 데이터를 조회합니다."""
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def set(self, key: str, value: Any, expire: int = 300) -> None:
        """데이터를 캐시에 저장합니다."""
        data = json.dumps(value)
        self.redis.set(key, data, ex=expire)

    async def delete(self, key: str) -> None:
        """캐시에서 데이터를 삭제합니다."""
        self.redis.delete(key)

    async def clear(self) -> None:
        """캐시를 모두 삭제합니다."""
        self.redis.flushdb()

    def close(self) -> None:
        """Redis 연결을 종료합니다."""
        self.redis.close()
