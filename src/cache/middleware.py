"""캐시를 위한 미들웨어 모듈입니다."""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from .redis import RedisCache


class CacheMiddleware(BaseHTTPMiddleware):
    """캐시를 위한 미들웨어입니다."""

    def __init__(self, app, cache: RedisCache):
        """캐시 미들웨어를 초기화합니다."""
        super().__init__(app)
        self.cache = cache

    async def dispatch(self, request: Request, call_next) -> Response:
        """요청을 처리하고 캐시를 적용합니다."""
        # GET 요청만 캐시
        if request.method != "GET":
            return await call_next(request)

        # 캐시 키 생성
        cache_key = f"{request.method}:{request.url.path}:{request.query_params}"

        # 캐시에서 응답 확인
        cached_response = await self.cache.get(cache_key)
        if cached_response:
            return Response(content=cached_response, media_type="application/json")

        # 캐시가 없는 경우 요청 처리
        response = await call_next(request)

        # 응답을 캐시에 저장
        if response.status_code == 200:
            await self.cache.set(cache_key, response.body, expire=300)  # 5분

        return response
