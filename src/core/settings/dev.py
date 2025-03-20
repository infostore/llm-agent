"""개발 환경 설정을 정의하는 모듈입니다."""

from .base import BaseSettings


class DevSettings(BaseSettings):
    """개발 환경 설정 클래스입니다."""

    # 환경 설정
    ENVIRONMENT: str = "development"

    # API 설정
    API_RELOAD: bool = True

    # 로깅 설정
    LOG_LEVEL: str = "DEBUG"

    # 데이터베이스 설정
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/llm_agent_dev"

    # Redis 설정
    REDIS_URL: str = "redis://localhost:6379/0"

    # 보안 설정
    SECRET_KEY: str = "dev-secret-key"

    # 요청 제한 설정
    RATE_LIMIT_REQUESTS: int = 1000
    RATE_LIMIT_PERIOD: int = 60

    class Config:
        """Pydantic 설정 클래스입니다."""

        env_file = ".env.development"
        case_sensitive = True
