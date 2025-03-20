"""캐싱 미들웨어 모듈입니다."""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from .redis import RedisCache


class CacheMiddleware(BaseHTTPMiddleware):
    """캐싱을 위한 미들웨어입니다."""

    def __init__(self, app, cache: RedisCache):
        """캐시 미들웨어를 초기화합니다."""
        super().__init__(app)
        self.cache = cache

    async def dispatch(self, request: Request, call_next):
        """요청을 처리하고 캐싱을 수행합니다."""
        # GET 요청만 캐싱
        if request.method != "GET":
            return await call_next(request)

        # 캐시 키 생성
        cache_key = f"{request.method}:{request.url.path}"

        # 캐시 확인
        cached_response = await self.cache.get(cache_key)
        if cached_response:
            return cached_response

        # 캐시가 없는 경우 요청 처리
        response = await call_next(request)

        # 응답 캐싱
        await self.cache.set(cache_key, response)

        return response
