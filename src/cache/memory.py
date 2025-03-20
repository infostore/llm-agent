"""메모리 캐시를 제공하는 모듈입니다."""

import time
from typing import Any, Dict, Optional, Tuple

from .base import BaseCache


class MemoryCache(BaseCache):
    """메모리 캐시 클래스입니다."""

    def __init__(self):
        """메모리 캐시를 초기화합니다."""
        self._cache: Dict[str, Tuple[Any, float]] = {}

    async def get(self, key: str) -> Optional[Any]:
        """캐시에서 데이터를 조회합니다."""
        if key not in self._cache:
            return None

        value, expire_time = self._cache[key]
        if expire_time > 0 and time.time() > expire_time:
            await self.delete(key)
            return None

        return value

    async def set(self, key: str, value: Any, expire: int = 300) -> None:
        """데이터를 캐시에 저장합니다."""
        expire_time = time.time() + expire if expire > 0 else 0
        self._cache[key] = (value, expire_time)

    async def delete(self, key: str) -> None:
        """캐시에서 데이터를 삭제합니다."""
        if key in self._cache:
            del self._cache[key]

    async def clear(self) -> None:
        """캐시를 모두 삭제합니다."""
        self._cache.clear()

    def close(self) -> None:
        """메모리 캐시를 정리합니다."""
        self._cache.clear()
