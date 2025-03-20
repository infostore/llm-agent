"""모니터링을 위한 미들웨어 모듈입니다."""

import time
from typing import Callable

from fastapi import Request, Response
from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator import Instrumentator

from .metrics import (
    HTTP_REQUEST_DURATION,
    HTTP_REQUEST_SIZE,
    HTTP_RESPONSE_SIZE,
    HTTP_REQUESTS_TOTAL,
)


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


class MonitoringMiddleware:
    """모니터링 미들웨어입니다."""

    def __init__(self, app):
        """모니터링 미들웨어를 초기화합니다.

        Args:
            app: FastAPI 애플리케이션
        """
        self.app = app
        self.instrumentator = Instrumentator()

    async def __call__(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """요청을 처리합니다.

        Args:
            request: FastAPI 요청
            call_next: 다음 미들웨어/라우트 핸들러

        Returns:
            Response: FastAPI 응답
        """
        # 요청 시작 시간
        start_time = time.time()

        # 요청 크기 측정
        request_size = 0
        if request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()
            request_size = len(body)

        # 응답 처리
        response = await call_next(request)
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        # 응답 크기 측정
        response_size = len(response_body)

        # 메트릭 기록
        duration = time.time() - start_time
        HTTP_REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
        ).observe(duration)

        HTTP_REQUEST_SIZE.labels(
            method=request.method,
            endpoint=request.url.path,
        ).observe(request_size)

        HTTP_RESPONSE_SIZE.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
        ).observe(response_size)

        HTTP_REQUESTS_TOTAL.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
        ).inc()

        # 응답 재구성
        response.body_iterator = iter([response_body])
        return response
