#!/bin/bash

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 환경 변수 확인
if [ -z "$ENVIRONMENT" ]; then
    echo -e "${RED}환경 변수가 설정되지 않았습니다.${NC}"
    echo -e "${YELLOW}사용법: ENVIRONMENT=production ./deploy.sh${NC}"
    exit 1
fi

echo -e "${YELLOW}LLM Agent 배포를 시작합니다... (환경: $ENVIRONMENT)${NC}"

# 의존성 설치
echo -e "\n${GREEN}의존성을 설치합니다...${NC}"
pip install -r requirements.txt

# 환경 변수 파일 확인
if [ ! -f ".env.$ENVIRONMENT" ]; then
    echo -e "${RED}환경 변수 파일을 찾을 수 없습니다: .env.$ENVIRONMENT${NC}"
    exit 1
fi

# 데이터베이스 마이그레이션
echo -e "\n${GREEN}데이터베이스 마이그레이션을 실행합니다...${NC}"
alembic upgrade head

# Elasticsearch 인덱스 생성
echo -e "\n${GREEN}Elasticsearch 인덱스를 생성합니다...${NC}"
python scripts/create_indices.py

# Redis 캐시 초기화
echo -e "\n${GREEN}Redis 캐시를 초기화합니다...${NC}"
python scripts/init_redis.py

# 서비스 재시작
echo -e "\n${GREEN}서비스를 재시작합니다...${NC}"
if [ "$ENVIRONMENT" = "production" ]; then
    sudo systemctl restart llm-agent
else
    pkill -f "uvicorn src.main:app"
    nohup uvicorn src.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
fi

echo -e "\n${GREEN}배포가 완료되었습니다!${NC}"
echo -e "${YELLOW}서비스 상태를 확인하려면 다음 명령어를 실행하세요:${NC}"
echo -e "curl http://localhost:8000/health"
