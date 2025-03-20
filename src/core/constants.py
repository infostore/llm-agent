"""애플리케이션에서 사용되는 상수들을 정의합니다."""

from typing import Final

# API 관련 상수
API_VERSION: Final[str] = "v1"
API_PREFIX: Final[str] = f"/api/{API_VERSION}"

# 인증 관련 상수
TOKEN_TYPE: Final[str] = "Bearer"
TOKEN_HEADER: Final[str] = "Authorization"

# 데이터베이스 관련 상수
DB_POOL_SIZE: Final[int] = 5
DB_MAX_OVERFLOW: Final[int] = 10
DB_POOL_TIMEOUT: Final[int] = 30

# 캐시 관련 상수
CACHE_DEFAULT_TTL: Final[int] = 300  # 5분
CACHE_KEY_PREFIX: Final[str] = "llm_agent:"

# 요청 제한 관련 상수
RATE_LIMIT_DEFAULT_REQUESTS: Final[int] = 100
RATE_LIMIT_DEFAULT_PERIOD: Final[int] = 60  # 1분

# 로깅 관련 상수
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"

# 모니터링 관련 상수
METRICS_PREFIX: Final[str] = "llm_agent"
DEFAULT_METRICS_PORT: Final[int] = 9090

# 에러 메시지 상수
ERROR_MESSAGES: Final[dict] = {
    "not_found": "요청한 리소스를 찾을 수 없습니다.",
    "unauthorized": "인증이 필요합니다.",
    "forbidden": "접근 권한이 없습니다.",
    "validation_error": "입력값이 유효하지 않습니다.",
    "rate_limit": "요청이 너무 많습니다. 잠시 후 다시 시도해주세요.",
    "internal_error": "서버 내부 오류가 발생했습니다.",
}
