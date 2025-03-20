"""저장소의 기본 클래스를 정의합니다."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..base import BaseModel


class BaseRepository(ABC):
    """기본 저장소 클래스입니다."""

    @abstractmethod
    async def create(self, model: BaseModel) -> BaseModel:
        """모델을 생성합니다.

        Args:
            model: 생성할 모델

        Returns:
            생성된 모델
        """
        pass

    @abstractmethod
    async def read(self, id: str) -> Optional[BaseModel]:
        """모델을 조회합니다.

        Args:
            id: 조회할 모델 ID

        Returns:
            조회된 모델, 없으면 None
        """
        pass

    @abstractmethod
    async def update(self, model: BaseModel) -> BaseModel:
        """모델을 업데이트합니다.

        Args:
            model: 업데이트할 모델

        Returns:
            업데이트된 모델
        """
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """모델을 삭제합니다.

        Args:
            id: 삭제할 모델 ID

        Returns:
            삭제 성공 여부
        """
        pass

    @abstractmethod
    async def list(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[BaseModel]:
        """모델 목록을 조회합니다.

        Args:
            skip: 건너뛸 레코드 수
            limit: 조회할 레코드 수
            filters: 필터 조건

        Returns:
            모델 목록
        """
        pass
