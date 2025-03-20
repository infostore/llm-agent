"""인증의 기본 클래스를 정의합니다."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from fastapi import Request


class Authenticator(ABC):
    """인증 기본 클래스입니다."""

    @abstractmethod
    async def authenticate(self, request: Request) -> Optional[Dict[str, Any]]:
        """요청을 인증합니다.

        Args:
            request: FastAPI 요청 객체

        Returns:
            인증된 사용자 정보, 인증 실패시 None
        """
        pass

    @abstractmethod
    async def create_token(self, user_data: Dict[str, Any]) -> str:
        """토큰을 생성합니다.

        Args:
            user_data: 사용자 정보

        Returns:
            생성된 토큰
        """
        pass

    @abstractmethod
    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """토큰을 검증합니다.

        Args:
            token: 검증할 토큰

        Returns:
            토큰이 유효하면 사용자 정보, 아니면 None
        """
        pass
