"""커스텀 예외 클래스들을 정의하는 모듈입니다."""

from typing import Any, Dict, Optional


class BaseError(Exception):
    """기본 예외 클래스입니다."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        """예외를 초기화합니다."""
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class ValidationError(BaseError):
    """유효성 검사 예외입니다."""

    def __init__(
        self,
        message: str = "유효성 검사 실패",
        details: Optional[Dict[str, Any]] = None,
    ):
        """유효성 검사 예외를 초기화합니다."""
        super().__init__(message, status_code=400, details=details)


class AuthenticationError(BaseError):
    """인증 예외입니다."""

    def __init__(
        self,
        message: str = "인증 실패",
        details: Optional[Dict[str, Any]] = None,
    ):
        """인증 예외를 초기화합니다."""
        super().__init__(message, status_code=401, details=details)


class AuthorizationError(BaseError):
    """권한 예외입니다."""

    def __init__(
        self,
        message: str = "권한 없음",
        details: Optional[Dict[str, Any]] = None,
    ):
        """권한 예외를 초기화합니다."""
        super().__init__(message, status_code=403, details=details)


class NotFoundError(BaseError):
    """리소스를 찾을 수 없는 예외입니다."""

    def __init__(
        self,
        message: str = "리소스를 찾을 수 없음",
        details: Optional[Dict[str, Any]] = None,
    ):
        """리소스를 찾을 수 없는 예외를 초기화합니다."""
        super().__init__(message, status_code=404, details=details)


class ConflictError(BaseError):
    """리소스 충돌 예외입니다."""

    def __init__(
        self,
        message: str = "리소스 충돌",
        details: Optional[Dict[str, Any]] = None,
    ):
        """리소스 충돌 예외를 초기화합니다."""
        super().__init__(message, status_code=409, details=details)


class RateLimitError(BaseError):
    """요청 제한 예외입니다."""

    def __init__(
        self,
        message: str = "요청 제한 초과",
        details: Optional[Dict[str, Any]] = None,
    ):
        """요청 제한 예외를 초기화합니다."""
        super().__init__(message, status_code=429, details=details)


class DatabaseError(BaseError):
    """데이터베이스 예외입니다."""

    def __init__(
        self,
        message: str = "데이터베이스 오류",
        details: Optional[Dict[str, Any]] = None,
    ):
        """데이터베이스 예외를 초기화합니다."""
        super().__init__(message, status_code=500, details=details)


class CacheError(BaseError):
    """캐시 예외입니다."""

    def __init__(
        self,
        message: str = "캐시 오류",
        details: Optional[Dict[str, Any]] = None,
    ):
        """캐시 예외를 초기화합니다."""
        super().__init__(message, status_code=500, details=details)


class ExternalServiceError(BaseError):
    """외부 서비스 예외입니다."""

    def __init__(
        self,
        message: str = "외부 서비스 오류",
        details: Optional[Dict[str, Any]] = None,
    ):
        """외부 서비스 예외를 초기화합니다."""
        super().__init__(message, status_code=502, details=details)
