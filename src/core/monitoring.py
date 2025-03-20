"""모니터링 설정을 관리하는 모듈입니다."""

from prometheus_client import Counter, Histogram, start_http_server
from prometheus_fastapi_instrumentator import Instrumentator

from .constants import DEFAULT_METRICS_PORT, METRICS_PREFIX
from .settings import get_settings

settings = get_settings()


# 메트릭 정의
REQUEST_COUNT = Counter(
    f"{METRICS_PREFIX}_http_requests_total",
    "총 HTTP 요청 수",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    f"{METRICS_PREFIX}_http_request_duration_seconds",
    "HTTP 요청 처리 시간",
    ["method", "endpoint"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
)


def init_monitoring(app) -> None:
    """모니터링을 초기화합니다.

    Args:
        app: FastAPI 애플리케이션
    """
    # Prometheus FastAPI Instrumentator 설정
    Instrumentator().instrument(app).expose(app)

    # 메트릭 서버 시작
    start_http_server(DEFAULT_METRICS_PORT)


def record_request_metric(
    method: str,
    endpoint: str,
    status: int,
    duration: float,
) -> None:
    """요청 메트릭을 기록합니다.

    Args:
        method: HTTP 메서드
        endpoint: 엔드포인트
        status: HTTP 상태 코드
        duration: 요청 처리 시간
    """
    REQUEST_COUNT.labels(
        method=method,
        endpoint=endpoint,
        status=status,
    ).inc()

    REQUEST_LATENCY.labels(
        method=method,
        endpoint=endpoint,
    ).observe(duration)
