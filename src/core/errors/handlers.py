"""예외 핸들러를 정의하는 모듈입니다."""

import logging
from typing import Any, Dict

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from redis.exceptions import RedisError

from .exceptions import (
    BaseError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
    RateLimitError,
    DatabaseError,
    CacheError,
    ExternalServiceError,
)

logger = logging.getLogger(__name__)


async def base_error_handler(request: Request, exc: BaseError) -> JSONResponse:
    """기본 예외 핸들러입니다."""
    logger.error(
        "예외 발생: %s, 상태 코드: %d, 상세: %s",
        exc.message,
        exc.status_code,
        exc.details,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "details": exc.details,
        },
    )


async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """유효성 검사 예외 핸들러입니다."""
    logger.error("유효성 검사 실패: %s", exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "유효성 검사 실패",
            "details": exc.errors(),
        },
    )


async def sqlalchemy_error_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """SQLAlchemy 예외 핸들러입니다."""
    logger.error("데이터베이스 오류: %s", str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "데이터베이스 오류",
            "details": {"error": str(exc)},
        },
    )


async def redis_error_handler(request: Request, exc: RedisError) -> JSONResponse:
    """Redis 예외 핸들러입니다."""
    logger.error("Redis 오류: %s", str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "캐시 오류",
            "details": {"error": str(exc)},
        },
    )


def register_error_handlers(app: Any) -> None:
    """예외 핸들러를 등록합니다."""
    # 커스텀 예외 핸들러
    app.add_exception_handler(BaseError, base_error_handler)
    app.add_exception_handler(ValidationError, base_error_handler)
    app.add_exception_handler(AuthenticationError, base_error_handler)
    app.add_exception_handler(AuthorizationError, base_error_handler)
    app.add_exception_handler(NotFoundError, base_error_handler)
    app.add_exception_handler(ConflictError, base_error_handler)
    app.add_exception_handler(RateLimitError, base_error_handler)
    app.add_exception_handler(DatabaseError, base_error_handler)
    app.add_exception_handler(CacheError, base_error_handler)
    app.add_exception_handler(ExternalServiceError, base_error_handler)

    # FastAPI 예외 핸들러
    app.add_exception_handler(RequestValidationError, validation_error_handler)

    # 외부 라이브러리 예외 핸들러
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(RedisError, redis_error_handler)
