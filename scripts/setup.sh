#!/bin/bash

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}LLM Agent 개발 환경 설정을 시작합니다...${NC}"

# Python 가상환경 생성
echo -e "\n${GREEN}Python 가상환경을 생성합니다...${NC}"
python -m venv venv
source venv/bin/activate

# 의존성 설치
echo -e "\n${GREEN}의존성을 설치합니다...${NC}"
pip install -r requirements.txt

# 환경 변수 파일 생성
echo -e "\n${GREEN}환경 변수 파일을 생성합니다...${NC}"
cp .env.example .env
cp .env.example .env.development
cp .env.example .env.production

# 데이터베이스 마이그레이션
echo -e "\n${GREEN}데이터베이스 마이그레이션을 실행합니다...${NC}"
alembic upgrade head

# Elasticsearch 인덱스 생성
echo -e "\n${GREEN}Elasticsearch 인덱스를 생성합니다...${NC}"
python scripts/create_indices.py

# Redis 캐시 초기화
echo -e "\n${GREEN}Redis 캐시를 초기화합니다...${NC}"
python scripts/init_redis.py

echo -e "\n${GREEN}개발 환경 설정이 완료되었습니다!${NC}"
echo -e "${YELLOW}다음 명령어로 서버를 실행할 수 있습니다:${NC}"
echo -e "uvicorn src.main:app --reload"
