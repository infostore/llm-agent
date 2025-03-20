"""Redis 이벤트 발행자를 구현합니다."""

import json
from typing import Optional

import redis.asyncio as redis
from .base import Event, EventPublisher

from core.settings import get_settings

settings = get_settings()


class RedisEventPublisher(EventPublisher):
    """Redis 이벤트 발행자입니다."""

    def __init__(
        self,
        redis_url: Optional[str] = None,
        channel_prefix: str = "events:",
    ):
        """Redis 이벤트 발행자를 초기화합니다.

        Args:
            redis_url: Redis URL
            channel_prefix: 채널 접두사
        """
        self.redis_url = redis_url or settings.REDIS_URL
        self.channel_prefix = channel_prefix
        self.redis: Optional[redis.Redis] = None

    async def connect(self) -> None:
        """Redis에 연결합니다."""
        if not self.redis:
            self.redis = redis.from_url(
                self.redis_url,
                encoding="utf8",
                decode_responses=True,
            )

    async def disconnect(self) -> None:
        """Redis 연결을 종료합니다."""
        if self.redis:
            await self.redis.close()
            self.redis = None

    async def publish(self, event: Event) -> None:
        """이벤트를 Redis에 발행합니다.

        Args:
            event: 발행할 이벤트
        """
        if not self.redis:
            await self.connect()
            if not self.redis:
                raise RuntimeError("Redis 연결에 실패했습니다.")

        channel = f"{self.channel_prefix}{event.event_type}"
        message = event.model_dump_json()
        await self.redis.publish(channel, message)
