"""Elasticsearch 검색 엔진 구현을 구현합니다."""

from typing import Any, Dict, List, Optional

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from .base import SearchEngine, SearchQuery, SearchResult

from core.settings import get_settings

settings = get_settings()


class ElasticsearchEngine(SearchEngine):
    """Elasticsearch 검색 엔진입니다."""

    def __init__(
        self,
        hosts: Optional[List[str]] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """Elasticsearch 엔진을 초기화합니다.

        Args:
            hosts: Elasticsearch 호스트 목록
            username: 사용자 이름
            password: 비밀번호
        """
        self.hosts = hosts or [settings.ELASTICSEARCH_URL]
        self.username = username or settings.ELASTICSEARCH_USERNAME
        self.password = password or settings.ELASTICSEARCH_PASSWORD
        self.client: Optional[AsyncElasticsearch] = None

    async def connect(self) -> None:
        """Elasticsearch에 연결합니다."""
        if not self.client:
            self.client = AsyncElasticsearch(
                hosts=self.hosts,
                basic_auth=(
                    (self.username, self.password)
                    if self.username and self.password
                    else None
                ),
            )

    async def disconnect(self) -> None:
        """Elasticsearch 연결을 종료합니다."""
        if self.client:
            await self.client.close()
            self.client = None

    async def index(self, index_name: str, document: Dict[str, Any]) -> None:
        """문서를 인덱싱합니다.

        Args:
            index_name: 인덱스 이름
            document: 인덱싱할 문서
        """
        if not self.client:
            await self.connect()
            if not self.client:
                raise RuntimeError("Elasticsearch 연결에 실패했습니다.")

        await self.client.index(index=index_name, document=document)

    async def bulk_index(
        self, index_name: str, documents: List[Dict[str, Any]]
    ) -> None:
        """여러 문서를 일괄 인덱싱합니다.

        Args:
            index_name: 인덱스 이름
            documents: 인덱싱할 문서 목록
        """
        if not self.client:
            await self.connect()
            if not self.client:
                raise RuntimeError("Elasticsearch 연결에 실패했습니다.")

        actions = [
            {
                "_index": index_name,
                "_source": document,
            }
            for document in documents
        ]
        await async_bulk(self.client, actions)

    async def search(self, index_name: str, query: SearchQuery) -> List[SearchResult]:
        """문서를 검색합니다.

        Args:
            index_name: 검색할 인덱스 이름
            query: 검색 쿼리

        Returns:
            검색 결과 목록
        """
        if not self.client:
            await self.connect()
            if not self.client:
                raise RuntimeError("Elasticsearch 연결에 실패했습니다.")

        # 검색 쿼리 구성
        search_query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": query.query,
                                "fields": ["*"],
                            }
                        }
                    ]
                }
            },
            "from": (query.page - 1) * query.page_size,
            "size": query.page_size,
        }

        # 필터 추가
        if query.filters:
            search_query["query"]["bool"]["filter"] = [
                {"term": {k: v}} for k, v in query.filters.items()
            ]

        # 정렬 추가
        if query.sort_by:
            search_query["sort"] = [{query.sort_by: {"order": query.sort_order}}]

        # 검색 실행
        response = await self.client.search(
            index=index_name,
            body=search_query,
        )

        # 결과 변환
        return [
            SearchResult(
                id=hit["_id"],
                score=hit["_score"],
                content=hit["_source"],
                metadata=hit.get("_metadata"),
            )
            for hit in response["hits"]["hits"]
        ]

    async def delete(self, index_name: str, document_id: str) -> None:
        """문서를 삭제합니다.

        Args:
            index_name: 인덱스 이름
            document_id: 삭제할 문서 ID
        """
        if not self.client:
            await self.connect()
            if not self.client:
                raise RuntimeError("Elasticsearch 연결에 실패했습니다.")

        await self.client.delete(index=index_name, id=document_id)

    async def update(
        self, index_name: str, document_id: str, document: Dict[str, Any]
    ) -> None:
        """문서를 업데이트합니다.

        Args:
            index_name: 인덱스 이름
            document_id: 업데이트할 문서 ID
            document: 업데이트할 문서 내용
        """
        if not self.client:
            await self.connect()
            if not self.client:
                raise RuntimeError("Elasticsearch 연결에 실패했습니다.")

        await self.client.update(
            index=index_name,
            id=document_id,
            body={"doc": document},
        )
