"""검색 시스템의 기본 클래스를 정의합니다."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class SearchResult(BaseModel):
    """검색 결과 모델입니다."""

    id: str
    score: float
    content: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


class SearchQuery(BaseModel):
    """검색 쿼리 모델입니다."""

    query: str
    filters: Optional[Dict[str, Any]] = None
    page: int = 1
    page_size: int = 10
    sort_by: Optional[str] = None
    sort_order: str = "desc"


class SearchEngine(ABC):
    """검색 엔진 기본 클래스입니다."""

    @abstractmethod
    async def connect(self) -> None:
        """검색 엔진에 연결합니다."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """검색 엔진 연결을 종료합니다."""
        pass

    @abstractmethod
    async def index(self, index_name: str, document: Dict[str, Any]) -> None:
        """문서를 인덱싱합니다.

        Args:
            index_name: 인덱스 이름
            document: 인덱싱할 문서
        """
        pass

    @abstractmethod
    async def bulk_index(
        self, index_name: str, documents: List[Dict[str, Any]]
    ) -> None:
        """여러 문서를 일괄 인덱싱합니다.

        Args:
            index_name: 인덱스 이름
            documents: 인덱싱할 문서 목록
        """
        pass

    @abstractmethod
    async def search(self, index_name: str, query: SearchQuery) -> List[SearchResult]:
        """문서를 검색합니다.

        Args:
            index_name: 검색할 인덱스 이름
            query: 검색 쿼리

        Returns:
            검색 결과 목록
        """
        pass

    @abstractmethod
    async def delete(self, index_name: str, document_id: str) -> None:
        """문서를 삭제합니다.

        Args:
            index_name: 인덱스 이름
            document_id: 삭제할 문서 ID
        """
        pass

    @abstractmethod
    async def update(
        self, index_name: str, document_id: str, document: Dict[str, Any]
    ) -> None:
        """문서를 업데이트합니다.

        Args:
            index_name: 인덱스 이름
            document_id: 업데이트할 문서 ID
            document: 업데이트할 문서 내용
        """
        pass
