"""모니터링 미들웨어 모듈입니다."""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram

# 메트릭 정의
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)


class MonitoringMiddleware(BaseHTTPMiddleware):
    """모니터링을 위한 미들웨어입니다."""

    async def dispatch(self, request: Request, call_next):
        """요청을 처리하고 메트릭을 수집합니다."""
        method = request.method
        endpoint = request.url.path

        # 요청 시작 시간 기록
        with REQUEST_LATENCY.labels(method=method, endpoint=endpoint).time():
            response = await call_next(request)

        # 요청 수 카운트 증가
        REQUEST_COUNT.labels(
            method=method, endpoint=endpoint, status=response.status_code
        ).inc()

        return response
