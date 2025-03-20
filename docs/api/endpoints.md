# API 엔드포인트

## 인증

### 로그인
- **POST** `/api/v1/auth/login`
- 사용자 인증 및 토큰 발급

### 토큰 갱신
- **POST** `/api/v1/auth/refresh`
- 리프레시 토큰을 사용하여 새로운 액세스 토큰 발급

### 로그아웃
- **POST** `/api/v1/auth/logout`
- 현재 세션 종료

## 사용자 관리

### 사용자 등록
- **POST** `/api/v1/users/register`
- 새로운 사용자 계정 생성

### 프로필 조회
- **GET** `/api/v1/users/me`
- 현재 로그인한 사용자의 프로필 정보 조회

### 프로필 수정
- **PUT** `/api/v1/users/me`
- 사용자 프로필 정보 수정

## LLM 대화

### 대화 시작
- **POST** `/api/v1/conversations`
- 새로운 대화 세션 시작

### 메시지 전송
- **POST** `/api/v1/conversations/{conversation_id}/messages`
- 대화에 메시지 추가

### 대화 내역 조회
- **GET** `/api/v1/conversations/{conversation_id}/messages`
- 특정 대화의 메시지 내역 조회

### 대화 목록 조회
- **GET** `/api/v1/conversations`
- 사용자의 대화 목록 조회

## 문서 관리

### 문서 업로드
- **POST** `/api/v1/documents`
- 새로운 문서 업로드

### 문서 조회
- **GET** `/api/v1/documents/{document_id}`
- 특정 문서의 상세 정보 조회

### 문서 목록 조회
- **GET** `/api/v1/documents`
- 사용자의 문서 목록 조회

### 문서 삭제
- **DELETE** `/api/v1/documents/{document_id}`
- 특정 문서 삭제

## 시스템

### 상태 확인
- **GET** `/api/v1/health`
- API 서버 상태 확인

### 메트릭스
- **GET** `/api/v1/metrics`
- Prometheus 메트릭스 조회

## 응답 형식

### 성공 응답
```json
{
    "status": "success",
    "data": {
        // 응답 데이터
    }
}
```

### 에러 응답
```json
{
    "status": "error",
    "error": {
        "code": "ERROR_CODE",
        "message": "에러 메시지",
        "details": {
            // 추가 에러 정보
        }
    }
}
``` 