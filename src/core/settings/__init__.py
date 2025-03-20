"""설정을 관리하는 패키지입니다."""

import os
from functools import lru_cache

from .base import BaseSettings
from .dev import DevSettings
from .prod import ProdSettings


def get_settings() -> BaseSettings:
    """환경에 따른 설정 객체를 반환합니다."""
    env = os.getenv("ENV", "development")

    if env == "production":
        return ProdSettings()
    return DevSettings()


__all__ = ["get_settings", "BaseSettings", "DevSettings", "ProdSettings"]
