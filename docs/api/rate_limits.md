# 레이트 리밋

## 개요

API 요청의 과도한 사용을 방지하기 위해 레이트 리밋이 적용됩니다. 각 엔드포인트별로 다른 제한이 적용될 수 있습니다.

## 기본 제한

### 개발 환경
- 요청 수: 1000회/분
- 동시 연결: 100개

### 운영 환경
- 요청 수: 100회/분
- 동시 연결: 50개

## 응답 헤더

레이트 리밋 관련 정보는 응답 헤더에 포함됩니다:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## 제한 초과 시

레이트 리밋을 초과하면 다음과 같은 응답을 받게 됩니다:

```json
{
    "detail": "요청 제한을 초과했습니다.",
    "code": "RATE_LIMIT_EXCEEDED",
    "retry_after": 60
}
```

## 제한 예외

다음 엔드포인트는 레이트 리밋이 적용되지 않습니다:
- `/api/v1/health`
- `/api/v1/metrics`

## 제한 증가 요청

제한 증가가 필요한 경우 다음 정보를 포함하여 요청하세요:
- 현재 사용량
- 증가가 필요한 이유
- 예상 사용량

## 모니터링

레이트 리밋 상태는 Prometheus를 통해 모니터링할 수 있습니다:
- `http_requests_total`
- `http_requests_in_flight`
- `rate_limit_exceeded_total` 