"""보안 미들웨어 모듈입니다."""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from .auth import verify_token


class SecurityMiddleware(BaseHTTPMiddleware):
    """보안을 위한 미들웨어입니다."""

    async def dispatch(self, request: Request, call_next):
        """요청을 처리하고 보안 검사를 수행합니다."""
        # 헬스 체크와 메트릭 엔드포인트는 인증 제외
        if request.url.path in ["/health", "/metrics"]:
            return await call_next(request)

        # 인증 토큰 검증
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다")

        try:
            token = auth_header.split(" ")[1]
            await verify_token(token)
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))

        return await call_next(request)
