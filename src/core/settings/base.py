"""기본 설정 클래스를 정의하는 모듈입니다."""

from typing import List
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    """기본 설정 클래스입니다."""

    # API 설정
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LLM Agent API"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True

    # OpenAI 설정
    OPENAI_API_KEY: str

    # 환경 설정
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # CORS 설정
    CORS_ORIGINS: List[str] = ["*"]

    # 데이터베이스 설정
    DATABASE_URL: str = "sqlite:///./app.db"

    # 보안 설정
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 캐시 설정
    REDIS_URL: str = "redis://localhost:6379/0"

    # 모니터링 설정
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090

    class Config:
        """Pydantic 설정 클래스입니다."""

        case_sensitive = True
        env_file = ".env"
