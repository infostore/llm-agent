"""메타데이터 믹스인을 구현합니다."""

from typing import Any, Dict, Optional

from pydantic import Field

from .base import BaseMixin


class MetadataMixin(BaseMixin):
    """메타데이터 믹스인입니다."""

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="추가 메타데이터",
    )

    def to_dict(self) -> dict:
        """모델을 딕셔너리로 변환합니다.

        Returns:
            딕셔너리 형태의 모델 데이터
        """
        return {"metadata": self.metadata}

    @classmethod
    def from_dict(cls, data: dict) -> "MetadataMixin":
        """딕셔너리로부터 모델을 생성합니다.

        Args:
            data: 모델 데이터 딕셔너리

        Returns:
            생성된 모델 인스턴스
        """
        return cls(**data)

    def update(self, data: dict) -> None:
        """모델을 업데이트합니다.

        Args:
            data: 업데이트할 데이터
        """
        if "metadata" in data:
            self.metadata.update(data["metadata"])

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """메타데이터 값을 가져옵니다.

        Args:
            key: 메타데이터 키
            default: 기본값

        Returns:
            메타데이터 값
        """
        return self.metadata.get(key, default)

    def set_metadata(self, key: str, value: Any) -> None:
        """메타데이터 값을 설정합니다.

        Args:
            key: 메타데이터 키
            value: 메타데이터 값
        """
        self.metadata[key] = value

    def remove_metadata(self, key: str) -> None:
        """메타데이터를 제거합니다.

        Args:
            key: 메타데이터 키
        """
        self.metadata.pop(key, None)
