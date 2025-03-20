"""운영 환경 설정을 정의하는 모듈입니다."""

from .base import BaseSettings


class ProdSettings(BaseSettings):
    """운영 환경 설정 클래스입니다."""

    # 환경 설정
    ENVIRONMENT: str = "production"

    # API 설정
    API_RELOAD: bool = False

    # 로깅 설정
    LOG_LEVEL: str = "INFO"

    # 데이터베이스 설정
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/llm_agent"

    # Redis 설정
    REDIS_URL: str = "redis://redis:6379/0"

    # 보안 설정
    SECRET_KEY: str  # 운영 환경에서는 반드시 환경 변수로 설정

    # 요청 제한 설정
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60

    class Config:
        """Pydantic 설정 클래스입니다."""

        env_file = ".env.production"
        case_sensitive = True
