"""FastAPI 애플리케이션의 메인 모듈입니다."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.api import api_router
from .core.config import get_settings

settings = get_settings()

app = FastAPI(
  title="LLM Agent API",
  description="LLM Agent를 위한 FastAPI 기반 REST API",
  version="1.0.0",
)

# CORS 설정
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# API 라우터 등록
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root() -> dict[str, str]:
  """루트 엔드포인트입니다."""
  return {"message": "LLM Agent API에 오신 것을 환영합니다!"}

@app.get("/health")
async def health_check() -> dict[str, str]:
  """헬스 체크 엔드포인트입니다."""
  return {"status": "healthy"} 