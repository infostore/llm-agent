"""요청 제한의 기본 클래스를 정의합니다."""

from abc import ABC, abstractmethod
from typing import Optional

from fastapi import Request


class RateLimiter(ABC):
    """요청 제한 기본 클래스입니다."""

    @abstractmethod
    async def is_rate_limited(self, request: Request) -> bool:
        """요청이 제한되었는지 확인합니다.

        Args:
            request: FastAPI 요청 객체

        Returns:
            요청이 제한되었으면 True, 아니면 False
        """
        pass

    @abstractmethod
    async def get_remaining_requests(self, request: Request) -> Optional[int]:
        """남은 요청 수를 반환합니다.

        Args:
            request: FastAPI 요청 객체

        Returns:
            남은 요청 수, 제한 정보를 가져올 수 없으면 None
        """
        pass

    @abstractmethod
    async def get_reset_time(self, request: Request) -> Optional[int]:
        """제한이 초기화되는 시간을 반환합니다.

        Args:
            request: FastAPI 요청 객체

        Returns:
            제한이 초기화되는 시간(초), 제한 정보를 가져올 수 없으면 None
        """
        pass
