"""JWT 인증 구현을 구현합니다."""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from fastapi import Request
from jose import JWTError, jwt

from .base import Authenticator

from core.settings import get_settings

settings = get_settings()


class JWTAuthenticator(Authenticator):
    """JWT 인증 구현입니다."""

    def __init__(
        self,
        secret_key: Optional[str] = None,
        algorithm: Optional[str] = None,
        access_token_expire_minutes: Optional[int] = None,
    ):
        """JWT 인증을 초기화합니다.

        Args:
            secret_key: 비밀 키
            algorithm: 알고리즘
            access_token_expire_minutes: 액세스 토큰 만료 시간(분)
        """
        self.secret_key = secret_key or settings.SECRET_KEY
        self.algorithm = algorithm or settings.ALGORITHM
        self.access_token_expire_minutes = (
            access_token_expire_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    async def authenticate(self, request: Request) -> Optional[Dict[str, Any]]:
        """요청을 인증합니다.

        Args:
            request: FastAPI 요청 객체

        Returns:
            인증된 사용자 정보, 인증 실패시 None
        """
        # Authorization 헤더 확인
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        # 토큰 추출 및 검증
        token = auth_header.split(" ")[1]
        return await self.verify_token(token)

    async def create_token(self, user_data: Dict[str, Any]) -> str:
        """토큰을 생성합니다.

        Args:
            user_data: 사용자 정보

        Returns:
            생성된 토큰
        """
        # 만료 시간 설정
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode = user_data.copy()
        to_encode.update({"exp": expire})

        # 토큰 생성
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """토큰을 검증합니다.

        Args:
            token: 검증할 토큰

        Returns:
            토큰이 유효하면 사용자 정보, 아니면 None
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
