#!/bin/bash

# 환경 변수 설정
ENV=${ENV:-development}

# 애플리케이션 실행
exec uvicorn src.main:app \
    --host ${API_HOST:-0.0.0.0} \
    --port ${API_PORT:-8000} \
    --reload ${API_RELOAD:-true} \
    --log-level ${LOG_LEVEL:-INFO} 