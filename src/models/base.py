"""데이터베이스 기본 모델입니다."""

from datetime import datetime, UTC
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime


class Base(DeclarativeBase):
    """모든 데이터베이스 모델의 기본 클래스입니다."""
   
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(UTC),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
        nullable=False
    ) 