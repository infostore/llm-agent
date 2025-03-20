"""모델의 기본 클래스를 정의합니다."""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class BaseModel(BaseModel):
    """기본 모델 클래스입니다."""

    id: Optional[str] = Field(None, description="모델 ID")
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="생성 시간",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="수정 시간",
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="추가 메타데이터",
    )

    class Config:
        """Pydantic 설정 클래스입니다."""

        from_attributes = True
