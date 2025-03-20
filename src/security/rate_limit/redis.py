"""Redis를 사용한 요청 제한 구현을 구현합니다."""

import time
from typing import Optional

from fastapi import Request
import redis.asyncio as redis

from .base import RateLimiter

from core.settings import get_settings

settings = get_settings()


class RedisRateLimiter(RateLimiter):
    """Redis를 사용한 요청 제한 구현입니다."""

    def __init__(
        self,
        redis_url: Optional[str] = None,
        requests_per_period: Optional[int] = None,
        period_in_seconds: Optional[int] = None,
    ):
        """Redis 요청 제한을 초기화합니다.

        Args:
            redis_url: Redis URL
            requests_per_period: 기간당 허용 요청 수
            period_in_seconds: 제한 기간(초)
        """
        self.redis_url = redis_url or settings.REDIS_URL
        self.requests_per_period = requests_per_period or settings.RATE_LIMIT_REQUESTS
        self.period_in_seconds = period_in_seconds or settings.RATE_LIMIT_PERIOD
        self.redis: Optional[redis.Redis] = None

    async def _get_redis(self) -> redis.Redis:
        """Redis 클라이언트를 가져옵니다.

        Returns:
            Redis 클라이언트
        """
        if not self.redis:
            self.redis = redis.from_url(self.redis_url)
        return self.redis

    def _get_key(self, request: Request) -> str:
        """요청에 대한 Redis 키를 생성합니다.

        Args:
            request: FastAPI 요청 객체

        Returns:
            Redis 키
        """
        # IP 주소를 기본 식별자로 사용
        client_ip = request.client.host
        return f"rate_limit:{client_ip}"

    async def is_rate_limited(self, request: Request) -> bool:
        """요청이 제한되었는지 확인합니다.

        Args:
            request: FastAPI 요청 객체

        Returns:
            요청이 제한되었으면 True, 아니면 False
        """
        redis_client = await self._get_redis()
        key = self._get_key(request)

        # 현재 요청 수 확인
        current = await redis_client.get(key)
        if not current:
            # 첫 요청이면 카운터 초기화
            await redis_client.setex(
                key,
                self.period_in_seconds,
                self.requests_per_period - 1,
            )
            return False

        current = int(current)
        if current <= 0:
            return True

        # 요청 수 감소
        await redis_client.decr(key)
        return False

    async def get_remaining_requests(self, request: Request) -> Optional[int]:
        """남은 요청 수를 반환합니다.

        Args:
            request: FastAPI 요청 객체

        Returns:
            남은 요청 수, 제한 정보를 가져올 수 없으면 None
        """
        redis_client = await self._get_redis()
        key = self._get_key(request)

        current = await redis_client.get(key)
        if not current:
            return self.requests_per_period

        return int(current)

    async def get_reset_time(self, request: Request) -> Optional[int]:
        """제한이 초기화되는 시간을 반환합니다.

        Args:
            request: FastAPI 요청 객체

        Returns:
            제한이 초기화되는 시간(초), 제한 정보를 가져올 수 없으면 None
        """
        redis_client = await self._get_redis()
        key = self._get_key(request)

        ttl = await redis_client.ttl(key)
        if ttl < 0:
            return None

        return ttl
