"""에러 처리를 위한 패키지입니다."""

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
from .handlers import register_error_handlers

__all__ = [
    "BaseError",
    "ValidationError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ConflictError",
    "RateLimitError",
    "DatabaseError",
    "CacheError",
    "ExternalServiceError",
    "register_error_handlers",
]
