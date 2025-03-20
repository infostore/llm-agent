"""추적 설정을 관리하는 패키지입니다."""

from .opentelemetry import init_tracing

__all__ = ["init_tracing"]
