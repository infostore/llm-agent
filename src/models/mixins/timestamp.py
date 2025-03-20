"""타임스탬프 믹스인을 구현합니다."""

from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import BaseMixin


class TimestampMixin(BaseMixin):
    """타임스탬프 믹스인입니다."""

    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="생성 시간",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="수정 시간",
    )

    def to_dict(self) -> dict:
        """모델을 딕셔너리로 변환합니다.

        Returns:
            딕셔너리 형태의 모델 데이터
        """
        return {
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TimestampMixin":
        """딕셔너리로부터 모델을 생성합니다.

        Args:
            data: 모델 데이터 딕셔너리

        Returns:
            생성된 모델 인스턴스
        """
        if "created_at" in data and data["created_at"]:
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data and data["updated_at"]:
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return cls(**data)

    def update(self, data: dict) -> None:
        """모델을 업데이트합니다.

        Args:
            data: 업데이트할 데이터
        """
        if "created_at" in data and data["created_at"]:
            self.created_at = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data and data["updated_at"]:
            self.updated_at = datetime.fromisoformat(data["updated_at"])
