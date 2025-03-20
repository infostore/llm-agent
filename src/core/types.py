"""애플리케이션에서 사용되는 타입들을 정의합니다."""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class Token(BaseModel):
    """JWT 토큰 모델입니다."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """JWT 토큰 데이터 모델입니다."""

    username: Optional[str] = None
    scopes: List[str] = []


class PaginationParams(BaseModel):
    """페이지네이션 파라미터 모델입니다."""

    page: int = 1
    size: int = 10
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "asc"


class PaginatedResponse(BaseModel):
    """페이지네이션 응답 모델입니다."""

    items: List[Any]
    total: int
    page: int
    size: int
    pages: int


class ErrorResponse(BaseModel):
    """에러 응답 모델입니다."""

    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class SuccessResponse(BaseModel):
    """성공 응답 모델입니다."""

    message: str
    data: Optional[Any] = None


# 유틸리티 타입
JSON = Dict[str, Any]
ResponseData = Union[Dict[str, Any], List[Any], Any]
