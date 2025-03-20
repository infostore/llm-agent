"""공통 Pydantic 스키마입니다."""

from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
  """에러 응답 스키마입니다."""
  detail: str
  code: Optional[str] = None


class SuccessResponse(BaseModel):
  """성공 응답 스키마입니다."""
  message: str
  data: Optional[dict] = None 