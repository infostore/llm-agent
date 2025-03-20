"""보안을 위한 미들웨어 모듈입니다."""

from typing import Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from .auth import verify_token


class SecurityMiddleware(BaseHTTPMiddleware):
    """보안을 위한 미들웨어입니다."""

    async def dispatch(self, request: Request, call_next: callable) -> Response:
        """요청을 처리합니다.

        Args:
            request: FastAPI 요청 객체
            call_next: 다음 미들웨어/라우트 핸들러

        Returns:
            FastAPI 응답 객체
        """
        # 인증이 필요한 경로인지 확인
        if self._requires_auth(request.url.path):
            # Authorization 헤더 확인
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return Response(
                    status_code=401,
                    content={"detail": "인증이 필요합니다."},
                )

            # 토큰 검증
            token = auth_header.split(" ")[1]
            subject = verify_token(token)
            if not subject:
                return Response(
                    status_code=401,
                    content={"detail": "유효하지 않은 토큰입니다."},
                )

            # 요청 상태에 사용자 정보 추가
            request.state.user_id = subject

        # 다음 미들웨어/라우트 핸들러 호출
        response = await call_next(request)
        return response

    def _requires_auth(self, path: str) -> bool:
        """인증이 필요한 경로인지 확인합니다.

        Args:
            path: 요청 경로

        Returns:
            인증이 필요하면 True, 아니면 False
        """
        # 인증이 필요하지 않은 경로 목록
        public_paths = [
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/api/v1/docs",
            "/api/v1/openapi.json",
        ]
        return not any(path.startswith(p) for p in public_paths)
