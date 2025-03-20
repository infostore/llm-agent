# 인증 가이드

## 개요

LLM Agent API는 JWT(JSON Web Token) 기반의 인증 시스템을 사용합니다. 모든 API 요청은 유효한 JWT 토큰이 필요합니다.

## 토큰 획득

### 로그인

```http
POST /api/v1/auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

응답:
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer",
    "expires_in": 3600
}
```

### 토큰 갱신

```http
POST /api/v1/auth/refresh
Authorization: Bearer <refresh_token>

{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 토큰 사용

### 요청 헤더

모든 API 요청에 다음과 같은 Authorization 헤더를 포함해야 합니다:

```http
Authorization: Bearer <access_token>
```

## 토큰 만료

- Access Token: 1시간
- Refresh Token: 7일

## 보안 고려사항

1. 토큰은 안전하게 저장하고 관리해야 합니다.
2. HTTPS를 통한 통신만 사용합니다.
3. 토큰이 노출된 경우 즉시 재발급 받아야 합니다.
4. 주기적으로 토큰을 갱신하는 것이 좋습니다.

## 에러 응답

### 401 Unauthorized

```json
{
    "detail": "인증에 실패했습니다.",
    "code": "AUTH_FAILED"
}
```

### 403 Forbidden

```json
{
    "detail": "접근 권한이 없습니다.",
    "code": "FORBIDDEN"
}
```

### 419 Token Expired

```json
{
    "detail": "토큰이 만료되었습니다.",
    "code": "TOKEN_EXPIRED"
}
``` 