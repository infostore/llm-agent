"""서비스의 기본 클래스를 정의합니다."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ServiceResponse(BaseModel):
    """서비스 응답 기본 모델입니다."""

    success: bool = True
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None


class Service(ABC):
    """서비스 기본 클래스입니다."""

    @abstractmethod
    async def initialize(self) -> None:
        """서비스를 초기화합니다."""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """서비스를 정리합니다."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """서비스 상태를 확인합니다.

        Returns:
            서비스가 정상이면 True, 아니면 False
        """
        pass

    @abstractmethod
    async def get_metrics(self) -> Dict[str, Any]:
        """서비스 메트릭을 가져옵니다.

        Returns:
            서비스 메트릭
        """
        pass


class CRUDService(Service):
    """CRUD 서비스 기본 클래스입니다."""

    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> ServiceResponse:
        """데이터를 생성합니다.

        Args:
            data: 생성할 데이터

        Returns:
            생성 결과
        """
        pass

    @abstractmethod
    async def read(self, id: str) -> ServiceResponse:
        """데이터를 조회합니다.

        Args:
            id: 조회할 데이터 ID

        Returns:
            조회 결과
        """
        pass

    @abstractmethod
    async def update(self, id: str, data: Dict[str, Any]) -> ServiceResponse:
        """데이터를 업데이트합니다.

        Args:
            id: 업데이트할 데이터 ID
            data: 업데이트할 데이터

        Returns:
            업데이트 결과
        """
        pass

    @abstractmethod
    async def delete(self, id: str) -> ServiceResponse:
        """데이터를 삭제합니다.

        Args:
            id: 삭제할 데이터 ID

        Returns:
            삭제 결과
        """
        pass

    @abstractmethod
    async def list(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
    ) -> ServiceResponse:
        """데이터 목록을 조회합니다.

        Args:
            skip: 건너뛸 레코드 수
            limit: 조회할 레코드 수
            filters: 필터 조건

        Returns:
            조회 결과
        """
        pass
