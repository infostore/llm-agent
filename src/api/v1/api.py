"""API 라우터를 통합하는 모듈입니다."""

from fastapi import APIRouter
from .endpoints import chat

api_router = APIRouter()

api_router.include_router(chat.router, prefix="/v1", tags=["chat"]) 