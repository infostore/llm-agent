# WebSocket API

## 개요

실시간 양방향 통신을 위한 WebSocket API를 제공합니다. LLM과의 대화, 실시간 알림 등을 지원합니다.

## 연결

```javascript
const ws = new WebSocket('ws://api.example.com/ws');

ws.onopen = () => {
    console.log('WebSocket 연결됨');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('메시지 수신:', data);
};

ws.onerror = (error) => {
    console.error('WebSocket 에러:', error);
};

ws.onclose = () => {
    console.log('WebSocket 연결 종료');
};
```

## 인증

연결 시 JWT 토큰을 쿼리 파라미터로 전달:

```javascript
const ws = new WebSocket(`ws://api.example.com/ws?token=${jwtToken}`);
```

## 메시지 형식

### 클라이언트 -> 서버

```json
{
    "type": "message",
    "data": {
        "content": "안녕하세요",
        "timestamp": "2024-01-01T00:00:00Z"
    }
}
```

### 서버 -> 클라이언트

```json
{
    "type": "response",
    "data": {
        "content": "안녕하세요! 무엇을 도와드릴까요?",
        "timestamp": "2024-01-01T00:00:01Z"
    }
}
```

## 메시지 타입

### 일반 메시지
- `type`: "message"
- 용도: 일반적인 대화 메시지

### 시스템 메시지
- `type`: "system"
- 용도: 시스템 상태, 알림 등

### 에러 메시지
- `type`: "error"
- 용도: 에러 알림

## 연결 관리

### 핑/퐁
30초마다 핑 메시지를 보내 연결을 유지합니다:

```json
{
    "type": "ping"
}
```

### 재연결
연결이 끊어지면 자동으로 재연결을 시도합니다:
- 최대 5회 시도
- 지수 백오프 적용
- 5회 실패 시 사용자에게 알림

## 제한사항

- 최대 메시지 크기: 1MB
- 연결당 최대 동시 요청: 10개
- 메시지 전송 주기: 최소 100ms 