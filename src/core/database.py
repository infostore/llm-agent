"""데이터베이스 설정을 관리하는 모듈입니다."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from .constants import DB_MAX_OVERFLOW, DB_POOL_SIZE, DB_POOL_TIMEOUT
from .settings import get_settings

settings = get_settings()


class Base(DeclarativeBase):
    """SQLAlchemy 기본 모델 클래스입니다."""

    pass


# 비동기 엔진 생성
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=DB_POOL_SIZE,
    max_overflow=DB_MAX_OVERFLOW,
    pool_timeout=DB_POOL_TIMEOUT,
    echo=settings.LOG_LEVEL == "DEBUG",
)


# 비동기 세션 팩토리 생성
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """데이터베이스 세션을 가져옵니다.

    Yields:
        AsyncSession: 데이터베이스 세션
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """데이터베이스를 초기화합니다."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """데이터베이스 연결을 종료합니다."""
    await engine.dispose()
