"""기본 설정을 정의하는 모듈입니다."""

from typing import List, Optional
from pydantic_settings import BaseSettings


class BaseSettings(BaseSettings):
    """기본 설정 클래스입니다."""

    # API 설정
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LLM Agent API"

    # CORS 설정
    CORS_ORIGINS: List[str] = ["*"]

    # 데이터베이스 설정
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/db"

    # Redis 설정
    REDIS_URL: str = "redis://localhost:6379/0"

    # RabbitMQ 설정
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"

    # OpenAI 설정
    OPENAI_API_KEY: str = ""

    # 보안 설정
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 로깅 설정
    LOG_LEVEL: str = "INFO"

    # API 설정
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = False

    # 캐시 설정
    CACHE_TTL: int = 300  # 5분

    # 요청 제한 설정
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # 1분

    class Config:
        """Pydantic 설정 클래스입니다."""

        env_file = ".env"
        case_sensitive = True
