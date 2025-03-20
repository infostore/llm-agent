"""설정 모듈을 초기화하고 내보내는 모듈입니다."""

import os
from typing import Optional

from .base import BaseConfig
from .dev import DevConfig
from .prod import ProdConfig


def get_settings() -> BaseConfig:
    """현재 환경에 맞는 설정을 반환합니다."""
    env = os.getenv("ENV", "dev")

    if env == "prod":
        return ProdConfig()
    return DevConfig()


# 전역 설정 인스턴스
settings: Optional[BaseConfig] = None


def init_settings() -> None:
    """전역 설정을 초기화합니다."""
    global settings
    settings = get_settings()


# 설정 초기화
init_settings()
