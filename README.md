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
│   │   ├── monitoring.py
│   │   ├── rate_limit.py
│   │   ├── security.py
│   │   ├── cache.py
│   │   ├── logging.py
│   │   ├── constants.py
│   │   └── types.py
│   ├── models/
│   │   └── database/
│   │       └── base.py
│   ├── schemas/
│   │   ├── common.py
│   │   └── validators/
│   ├── services/
│   │   └── base.py
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
- `.env.example`을 참고하여 `.env` 파일을 생성합니다.
- OpenAI API 키를 설정해야 합니다.

4. 데이터베이스 마이그레이션:
```bash
alembic upgrade head
```

## 실행 방법

### 개발 환경
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker 환경
```bash
docker-compose up -d
```

## API 문서

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 엔드포인트

### 기본 엔드포인트
- `GET /`: 루트 엔드포인트
- `GET /health`: 헬스 체크 엔드포인트
- `GET /metrics`: Prometheus 메트릭

## 개발 가이드

자세한 개발 가이드는 `docs/development/` 디렉토리를 참고하세요.

## 테스트

### 단위 테스트
```bash
pytest tests/unit
```

### 통합 테스트
```bash
pytest tests/integration
```

### 전체 테스트
```bash
pytest
```

## 코드 품질

### 린트
```bash
flake8
black .
isort .
```

### 타입 체크
```bash
mypy .
```

## 배포

### 스크립트를 통한 배포
```bash
./scripts/deploy.sh
```

### Docker를 통한 배포
```bash
docker-compose -f docker-compose.prod.yml up -d
```
