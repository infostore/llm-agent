# API 문서

## 개요

LLM Agent API는 FastAPI를 기반으로 한 RESTful API 서비스입니다. 이 문서는 API의 사용 방법과 엔드포인트에 대한 상세한 설명을 제공합니다.

## API 버전

현재 API는 두 가지 버전을 지원합니다:

- [v1 API](./v1/README.md)
- [v2 API](./v2/README.md)

## 인증

모든 API 요청은 JWT 토큰을 통한 인증이 필요합니다. 인증 방법에 대한 자세한 내용은 [인증 가이드](./authentication.md)를 참고하세요.

## 요청 제한

API 요청은 레이트 리밋이 적용됩니다. 자세한 내용은 [레이트 리밋](./rate_limits.md)을 참고하세요.

## 에러 처리

API는 표준화된 에러 응답 형식을 사용합니다. 자세한 내용은 [에러 처리](./error_handling.md)를 참고하세요.

## 웹소켓

실시간 통신을 위한 웹소켓 API도 제공됩니다. 자세한 내용은 [웹소켓 API](./websocket.md)를 참고하세요. 