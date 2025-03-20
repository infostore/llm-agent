#!/bin/bash

# 환경 변수 설정
ENV=${ENV:-development}

# 환경에 따른 설정 파일 적용
if [ "$ENV" = "production" ]; then
    echo "Applying production settings..."
    cp .env.production .env
else
    echo "Applying development settings..."
    cp .env.development .env
fi

# 애플리케이션 실행
exec uvicorn src.main:app \
    --host ${API_HOST:-0.0.0.0} \
    --port ${API_PORT:-8000} \
    --reload ${API_RELOAD:-true} \
    --log-level ${LOG_LEVEL:-INFO} 