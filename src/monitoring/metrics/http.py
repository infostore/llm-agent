"""HTTP 메트릭을 정의합니다."""

from prometheus_client import Counter, Histogram

# HTTP 요청 지연 시간
HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP 요청 처리 시간",
    ["method", "endpoint", "status"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
)

# HTTP 요청 크기
HTTP_REQUEST_SIZE = Histogram(
    "http_request_size_bytes",
    "HTTP 요청 크기",
    ["method", "endpoint"],
    buckets=[100, 1000, 10000, 100000, 1000000],
)

# HTTP 응답 크기
HTTP_RESPONSE_SIZE = Histogram(
    "http_response_size_bytes",
    "HTTP 응답 크기",
    ["method", "endpoint", "status"],
    buckets=[100, 1000, 10000, 100000, 1000000],
)

# HTTP 요청 수
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "총 HTTP 요청 수",
    ["method", "endpoint", "status"],
)
