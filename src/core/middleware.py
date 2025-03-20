"""미들웨어 설정을 관리하는 모듈입니다."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .constants import CORS_ORIGINS
from .settings import get_settings

settings = get_settings()


def setup_middleware(app: FastAPI) -> None:
    """미들웨어를 설정합니다.

    Args:
        app: FastAPI 애플리케이션
    """
    # CORS 미들웨어 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 보안 미들웨어 설정
    @app.middleware("http")
    async def security_middleware(request, call_next):
        """보안 미들웨어입니다."""
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        return response

    # 요청 로깅 미들웨어 설정
    @app.middleware("http")
    async def logging_middleware(request, call_next):
        """로깅 미들웨어입니다."""
        response = await call_next(request)
        print(f"{request.method} {request.url.path} - {response.status_code}")
        return response
