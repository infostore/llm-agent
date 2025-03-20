"""코어 기능을 제공하는 패키지입니다."""

from .cache import clear_cache, get_cache, init_cache
from .database import Base, close_db, get_db, init_db
from .dependencies import (
    get_current_active_user,
    get_current_user,
    get_settings_dependency,
)
from .errors import (
    AuthenticationError,
    AuthorizationError,
    BaseError,
    CacheError,
    ConflictError,
    DatabaseError,
    ExternalServiceError,
    NotFoundError,
    RateLimitError,
    ValidationError,
    register_error_handlers,
)
from .logging import get_logger, setup_logging
from .middleware import setup_middleware
from .monitoring import init_monitoring, record_request_metric
from .rate_limit import RateLimiter, rate_limit_middleware
from .security import (
    create_access_token,
    get_password_hash,
    verify_password,
    verify_token,
)
from .settings import get_settings

__all__ = [
    # 데이터베이스
    "Base",
    "get_db",
    "init_db",
    "close_db",
    # 캐시
    "get_cache",
    "init_cache",
    "clear_cache",
    # 의존성
    "get_current_user",
    "get_current_active_user",
    "get_settings_dependency",
    # 에러
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
    # 로깅
    "setup_logging",
    "get_logger",
    # 미들웨어
    "setup_middleware",
    # 모니터링
    "init_monitoring",
    "record_request_metric",
    # 요청 제한
    "RateLimiter",
    "rate_limit_middleware",
    # 보안
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "verify_token",
    # 설정
    "get_settings",
]
