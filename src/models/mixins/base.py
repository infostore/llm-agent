"""믹스인의 기본 클래스를 정의합니다."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from pydantic import BaseModel


class BaseMixin(BaseModel):
    """기본 믹스인 클래스입니다."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """모델을 딕셔너리로 변환합니다.

        Returns:
            딕셔너리 형태의 모델 데이터
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseMixin":
        """딕셔너리로부터 모델을 생성합니다.

        Args:
            data: 모델 데이터 딕셔너리

        Returns:
            생성된 모델 인스턴스
        """
        pass

    @abstractmethod
    def update(self, data: Dict[str, Any]) -> None:
        """모델을 업데이트합니다.

        Args:
            data: 업데이트할 데이터
        """
        pass
