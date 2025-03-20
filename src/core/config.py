"""환경 설정을 관리하는 모듈입니다."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
  """애플리케이션 설정 클래스입니다."""
  
  # API 설정
  api_host: str = "0.0.0.0"
  api_port: int = 8000
  api_reload: bool = True
  
  # OpenAI 설정
  openai_api_key: str
  
  # 환경 설정
  environment: str = "development"
  log_level: str = "INFO"
  
  class Config:
    """Pydantic 설정입니다."""
    env_file = ".env"
    case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
  """설정 객체를 반환합니다."""
  return Settings() 