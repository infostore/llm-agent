"""요청 제한 설정을 관리하는 모듈입니다."""

from datetime import datetime, timedelta
from typing import Dict, Optional

import redis.asyncio as redis
from fastapi import HTTPException, Request, status

from .constants import RATE_LIMIT_DEFAULT_PERIOD, RATE_LIMIT_DEFAULT_REQUESTS
from .settings import get_settings

settings = get_settings()


class RateLimiter:
    """요청 제한을 관리하는 클래스입니다."""

    def __init__(
        self,
        redis_client: redis.Redis,
        requests: int = RATE_LIMIT_DEFAULT_REQUESTS,
        period: int = RATE_LIMIT_DEFAULT_PERIOD,
    ):
        """요청 제한기를 초기화합니다.

        Args:
            redis_client: Redis 클라이언트
            requests: 허용된 요청 수
            period: 제한 기간 (초)
        """
        self.redis = redis_client
        self.requests = requests
        self.period = period

    async def is_rate_limited(self, key: str) -> bool:
        """요청이 제한되었는지 확인합니다.

        Args:
            key: 요청 키

        Returns:
            bool: 제한 여부
        """
        current = await self.redis.get(key)
        if current is None:
            await self.redis.setex(key, self.period, 1)
            return False

        current = int(current)
        if current >= self.requests:
            return True

        await self.redis.incr(key)
        return False

    async def get_remaining_requests(self, key: str) -> int:
        """남은 요청 수를 가져옵니다.

        Args:
            key: 요청 키

        Returns:
            int: 남은 요청 수
        """
        current = await self.redis.get(key)
        if current is None:
            return self.requests
        return max(0, self.requests - int(current))

    async def get_reset_time(self, key: str) -> Optional[datetime]:
        """제한이 초기화되는 시간을 가져옵니다.

        Args:
            key: 요청 키

        Returns:
            Optional[datetime]: 초기화 시간
        """
        ttl = await self.redis.ttl(key)
        if ttl > 0:
            return datetime.utcnow() + timedelta(seconds=ttl)
        return None


async def rate_limit_middleware(
    request: Request,
    call_next,
    limiter: RateLimiter,
) -> Response:
    """요청 제한 미들웨어입니다.

    Args:
        request: FastAPI 요청
        call_next: 다음 미들웨어/라우트 핸들러
        limiter: 요청 제한기

    Returns:
        Response: FastAPI 응답

    Raises:
        HTTPException: 요청이 제한된 경우
    """
    key = f"rate_limit:{request.client.host}"
    if await limiter.is_rate_limited(key):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="요청이 너무 많습니다. 잠시 후 다시 시도해주세요.",
        )

    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(limiter.requests)
    response.headers["X-RateLimit-Remaining"] = str(
        await limiter.get_remaining_requests(key),
    )
    reset_time = await limiter.get_reset_time(key)
    if reset_time:
        response.headers["X-RateLimit-Reset"] = reset_time.isoformat()

    return response
