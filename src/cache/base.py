"""캐시 시스템의 기본 인터페이스를 정의하는 모듈입니다."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseCache(ABC):
    """캐시 시스템의 기본 인터페이스입니다."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """캐시에서 데이터를 조회합니다."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: int = 300) -> None:
        """데이터를 캐시에 저장합니다."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """캐시에서 데이터를 삭제합니다."""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """캐시를 모두 삭제합니다."""
        pass

    @abstractmethod
    def close(self) -> None:
        """캐시 연결을 종료합니다."""
        pass
