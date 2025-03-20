"""로깅 설정을 관리하는 모듈입니다."""

import logging
import sys
from typing import Optional

from .constants import LOG_DATE_FORMAT, LOG_FORMAT
from .settings import get_settings

settings = get_settings()


def setup_logging(
    level: Optional[str] = None,
    format_string: Optional[str] = None,
    date_format: Optional[str] = None,
) -> None:
    """로깅을 설정합니다.

    Args:
        level: 로깅 레벨
        format_string: 로그 포맷 문자열
        date_format: 날짜 포맷 문자열
    """
    # 로깅 레벨 설정
    log_level = level or settings.LOG_LEVEL
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # 포맷 설정
    fmt = format_string or LOG_FORMAT
    date_fmt = date_format or LOG_DATE_FORMAT

    # 기본 로거 설정
    logging.basicConfig(
        level=numeric_level,
        format=fmt,
        datefmt=date_fmt,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

    # FastAPI 로거 설정
    logging.getLogger("uvicorn").setLevel(numeric_level)
    logging.getLogger("uvicorn.access").setLevel(numeric_level)

    # SQLAlchemy 로거 설정
    logging.getLogger("sqlalchemy.engine").setLevel(numeric_level)
    logging.getLogger("sqlalchemy.pool").setLevel(numeric_level)

    # Redis 로거 설정
    logging.getLogger("redis").setLevel(numeric_level)


def get_logger(name: str) -> logging.Logger:
    """로거를 가져옵니다.

    Args:
        name: 로거 이름

    Returns:
        logging.Logger: 로거 인스턴스
    """
    return logging.getLogger(name)
