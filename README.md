# LLM Agent API

FastAPI 기반의 LLM Agent API 프로젝트입니다.

## 프로젝트 구조

```
.
├── src/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   └── api.py
│   │   └── v2/
│   │       └── __init__.py
│   ├── core/
│   │   ├── config/
│   │   │   ├── base.py
│   │   │   ├── dev.py
│   │   │   └── prod.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── errors/
│   │   │   ├── handlers.py
│   │   │   └── exceptions.py
│   │   ├── middleware.py
│   │   ├── monitoring/
│   │   │   ├── middleware.py
│   │   │   ├── metrics/
│   │   │   ├── logging/
│   │   │   └── tracing/
│   │   ├── rate_limit/
│   │   │   ├── base.py
│   │   │   └── redis.py
│   │   ├── security/
│   │   │   ├── auth/
│   │   │   │   ├── base.py
│   │   │   │   └── jwt.py
│   │   │   └── encryption/
│   │   │       ├── base.py
│   │   │       └── aes.py
│   │   ├── cache.py
│   │   ├── logging.py
│   │   ├── constants.py
│   │   └── types.py
│   ├── models/
│   │   ├── base.py
│   │   ├── mixins/
│   │   │   ├── base.py
│   │   │   ├── timestamp.py
│   │   │   └── metadata.py
│   │   └── repositories/
│   │       ├── base.py
│   │       └── __init__.py
│   ├── schemas/
│   │   ├── common.py
│   │   └── validators/
│   ├── services/
│   │   ├── base.py
│   │   └── __init__.py
│   ├── utils/
│   │   ├── security.py
│   │   └── validators.py
│   ├── workers/
│   │   ├── __init__.py
│   │   └── tasks.py
│   ├── __init__.py
│   └── main.py
├── alembic/
│   ├── versions/
│   │   └── 001_initial.py
│   └── env.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── integration/
│   ├── unit/
│   ├── fixtures/
│   ├── api/
│   ├── services/
│   └── utils/
├── docs/
│   ├── api/
│   ├── architecture/
│   ├── deployment/
│   └── development/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── scripts/
│   ├── setup.sh
│   └── deploy.sh
├── .github/
│   └── workflows/
│       ├── test.yml
│       ├── lint.yml
│       └── deploy.yml
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .pre-commit-config.yaml
├── .editorconfig
├── .env.example
├── .env.development
├── .env.production
├── .env
└── README.md
```

## 주요 기능

- FastAPI 기반 REST API
- JWT 기반 인증
- AES 암호화
- Redis 기반 캐싱
- Elasticsearch 검색
- RabbitMQ 메시지 큐
- Prometheus/Grafana 모니터링
- OpenTelemetry 분산 추적
- Alembic 데이터베이스 마이그레이션
- Celery 비동기 작업 처리

## 설치 방법

1. 가상환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 의존성 설치:
```bash
# 개발 환경
pip install -r requirements/dev.txt

# 운영 환경
pip install -r requirements/prod.txt
```

3. 환경 변수 설정:
```bash
# 개발 환경
cp .env.example .env.development

# 운영 환경
cp .env.example .env.production
```

4. 데이터베이스 마이그레이션:
```bash
alembic upgrade head
```

5. Elasticsearch 인덱스 생성:
```bash
python scripts/create_indices.py
```

6. Redis 캐시 초기화:
```bash
python scripts/init_redis.py
```

## 실행 방법

### 개발 환경
```bash
# 서버 실행
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Celery 워커 실행
celery -A src.workers.tasks worker --loglevel=info
```

### Docker 환경
```bash
# 개발 환경
docker-compose -f docker-compose.dev.yml up -d

# 운영 환경
docker-compose -f docker-compose.prod.yml up -d
```

## API 문서

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 모니터링

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- Jaeger: http://localhost:16686

## 개발 가이드

### 코드 품질 관리
```bash
# pre-commit 설치
pip install pre-commit
pre-commit install

# 코드 포맷팅
black .
isort .

# 린트
flake8
mypy .

# 보안 검사
bandit -r src/
```

### 테스트
```bash
# 단위 테스트
pytest tests/unit

# 통합 테스트
pytest tests/integration

# 전체 테스트
pytest

# 커버리지 리포트
pytest --cov=src tests/
```

### 배포
```bash
# 개발 환경
ENVIRONMENT=development ./scripts/deploy.sh

# 운영 환경
ENVIRONMENT=production ./scripts/deploy.sh
```

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.
