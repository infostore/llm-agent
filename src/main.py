"""FastAPI 애플리케이션의 메인 모듈입니다."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.api import api_router
from .core.settings import get_settings
from .monitoring.middleware import MonitoringMiddleware
from .security.middleware import SecurityMiddleware
from .cache.middleware import CacheMiddleware
from .cache.redis import RedisCache

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="LLM Agent를 위한 FastAPI 기반 REST API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Redis 캐시 초기화
redis_cache = RedisCache()

# 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(MonitoringMiddleware)
app.add_middleware(SecurityMiddleware)
app.add_middleware(CacheMiddleware, cache=redis_cache)

# API 라우터 등록
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root() -> dict[str, str]:
    """루트 엔드포인트입니다."""
    return {"message": "LLM Agent API에 오신 것을 환영합니다!"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    """헬스 체크 엔드포인트입니다."""
    return {"status": "healthy"}


@app.get("/metrics")
async def metrics() -> dict[str, str]:
    """Prometheus 메트릭 엔드포인트입니다."""
    return {"status": "ok"}
