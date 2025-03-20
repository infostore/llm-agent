# 개발 가이드

## 시작하기

### 개발 환경 설정
1. [개발 환경 구성](./setup.md)
   - Python 가상환경 설정
   - 의존성 설치
   - 환경 변수 설정

2. [IDE 설정](./ide_setup.md)
   - VS Code 설정
   - 디버깅 구성
   - 코드 스타일 설정

### 프로젝트 구조
```
src/
├── api/          # API 엔드포인트
├── core/         # 핵심 기능
├── models/       # 데이터 모델
├── services/     # 비즈니스 로직
├── utils/        # 유틸리티 함수
└── config/       # 설정 파일
```

## 개발 워크플로우

### 코드 품질 관리
1. [코드 스타일](./code_style.md)
   - PEP 8 준수
   - 타입 힌트 사용
   - 문서화 가이드

2. [테스트](./testing.md)
   - 단위 테스트
   - 통합 테스트
   - 테스트 커버리지

### 버전 관리
1. [Git 워크플로우](./git_workflow.md)
   - 브랜치 전략
   - 커밋 메시지 규칙
   - PR 프로세스

2. [CI/CD](./ci_cd.md)
   - GitHub Actions
   - 자동화된 테스트
   - 배포 파이프라인

## API 개발

### 엔드포인트 추가
1. [라우터 구성](./routing.md)
   - URL 구조
   - HTTP 메서드
   - 요청/응답 처리

2. [미들웨어](./middleware.md)
   - 인증
   - 로깅
   - 에러 처리

### 데이터베이스 작업
1. [모델 정의](./models.md)
   - SQLAlchemy 모델
   - 관계 설정
   - 마이그레이션

2. [쿼리 작성](./queries.md)
   - CRUD 작업
   - 조인
   - 트랜잭션

## 테스트

### 단위 테스트
```python
def test_user_creation():
    user = User(email="test@example.com")
    assert user.email == "test@example.com"
```

### 통합 테스트
```python
def test_user_registration():
    response = client.post("/api/v1/users/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
```

## 디버깅

### 로깅
```python
import logging

logger = logging.getLogger(__name__)
logger.info("작업 시작")
logger.error("에러 발생", exc_info=True)
```

### 디버거 사용
```python
import pdb

def complex_function():
    pdb.set_trace()  # 디버거 중단점
    # 코드 계속...
```

## 배포

### 개발 환경
```bash
# 서버 실행
uvicorn src.main:app --reload

# 테스트 실행
pytest

# 린트 검사
flake8
```

### 운영 환경
```bash
# 서버 실행
gunicorn src.main:app

# 모니터링
prometheus_client
```

## 문제 해결

### 일반적인 문제
1. [데이터베이스 연결](./troubleshooting/database.md)
2. [캐시 문제](./troubleshooting/cache.md)
3. [API 오류](./troubleshooting/api.md)

### 성능 최적화
1. [쿼리 최적화](./optimization/queries.md)
2. [캐시 전략](./optimization/cache.md)
3. [비동기 처리](./optimization/async.md) 