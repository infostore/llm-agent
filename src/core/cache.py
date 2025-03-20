"""캐시 설정을 관리하는 모듈입니다."""

from typing import Any, Optional

import redis.asyncio as redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from .constants import CACHE_DEFAULT_TTL, CACHE_KEY_PREFIX
from .settings import get_settings

settings = get_settings()


async def init_cache() -> None:
    """캐시를 초기화합니다."""
    redis_client = redis.from_url(
        settings.REDIS_URL,
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(
        RedisBackend(redis_client),
        prefix=CACHE_KEY_PREFIX,
        key_builder=lambda *args, **kwargs: f"{args[0].url.path}:{kwargs.get('query')}",
    )


def get_cache(
    expire: int = CACHE_DEFAULT_TTL,
    key_builder: Optional[callable] = None,
) -> Any:
    """캐시 데코레이터를 가져옵니다.

    Args:
        expire: 캐시 만료 시간 (초)
        key_builder: 캐시 키 생성 함수

    Returns:
        Any: 캐시 데코레이터
    """
    return cache(expire=expire, key_builder=key_builder)


async def clear_cache() -> None:
    """캐시를 초기화합니다."""
    await FastAPICache.get_backend().clear()
