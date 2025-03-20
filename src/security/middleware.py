"""보안을 위한 미들웨어 모듈입니다."""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from .auth import verify_token


class SecurityMiddleware(BaseHTTPMiddleware):
    """보안을 위한 미들웨어입니다."""

    async def dispatch(self, request: Request, call_next) -> Response:
        """요청을 처리하고 보안 검사를 수행합니다."""
        # 헬스 체크와 메트릭 엔드포인트는 인증 제외
        if request.url.path in ["/health", "/metrics"]:
            return await call_next(request)

        # API 문서 엔드포인트는 인증 제외
        if request.url.path.startswith("/api/docs") or request.url.path.startswith(
            "/api/redoc"
        ):
            return await call_next(request)

        # 토큰 검증
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(status_code=401, content={"detail": "인증이 필요합니다."})

        token = auth_header.split(" ")[1]
        if not verify_token(token):
            return Response(
                status_code=401, content={"detail": "유효하지 않은 토큰입니다."}
            )

        return await call_next(request)
