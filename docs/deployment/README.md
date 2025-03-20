# 배포 가이드

## 개요

이 문서는 LLM Agent의 배포 프로세스와 운영 환경 설정에 대한 가이드를 제공합니다.

## 배포 환경

### 요구사항
- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Elasticsearch 7+
- RabbitMQ 3.8+
- Docker 20.10+

### 시스템 요구사항
- CPU: 4코어 이상
- RAM: 16GB 이상
- 디스크: 100GB 이상 SSD
- 네트워크: 1Gbps 이상

## 배포 방법

### Docker Compose 사용
```yaml
version: "3.8"
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
    depends_on:
      - db
      - redis
      - elasticsearch
      - rabbitmq

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=llm_agent
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=secret

  redis:
    image: redis:6
    ports:
      - "6379:6379"

  elasticsearch:
    image: elasticsearch:7.17.0
    ports:
      - "9200:9200"

  rabbitmq:
    image: rabbitmq:3.8-management
    ports:
      - "5672:5672"
      - "15672:15672"
```

### 수동 배포
1. [서버 설정](./server_setup.md)
   - 시스템 업데이트
   - 필요한 패키지 설치
   - 방화벽 설정

2. [데이터베이스 설정](./database_setup.md)
   - PostgreSQL 설치
   - 데이터베이스 생성
   - 사용자 권한 설정

3. [애플리케이션 배포](./app_deployment.md)
   - 코드 배포
   - 의존성 설치
   - 서비스 설정

## 환경 설정

### 환경 변수
```bash
# .env.production
DATABASE_URL=postgresql://user:password@localhost:5432/llm_agent
REDIS_URL=redis://localhost:6379/0
ELASTICSEARCH_URL=http://localhost:9200
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
JWT_SECRET=your-secret-key
```

### 로깅 설정
```python
# logging.conf
[loggers]
keys=root,app

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler,fileHandler

[logger_app]
level=INFO
handlers=fileHandler
qualname=app
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=INFO
formatter=simpleFormatter
args=('app.log', 'a')

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## 모니터링

### Prometheus 설정
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'llm_agent'
    static_configs:
      - targets: ['localhost:8000']
```

### Grafana 대시보드
- API 응답 시간
- 에러율
- 리소스 사용량
- 비즈니스 메트릭스

## 백업 및 복구

### 데이터베이스 백업
```bash
# 백업
pg_dump -U admin llm_agent > backup.sql

# 복구
psql -U admin llm_agent < backup.sql
```

### 로그 관리
```bash
# 로그 로테이션
/var/log/llm_agent/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 www-data www-data
}
```

## 보안

### SSL/TLS 설정
```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name api.example.com;

    ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;
}
```

### 방화벽 설정
```bash
# UFW 설정
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp
```

## 확장

### 로드 밸런서 설정
```nginx
upstream llm_agent {
    server 10.0.0.1:8000;
    server 10.0.0.2:8000;
    server 10.0.0.3:8000;
}
```

### 데이터베이스 샤딩
```sql
-- 샤딩 키 설정
ALTER TABLE users SET (sharding_key = 'id');
```

## 문제 해결

### 일반적인 문제
1. [연결 문제](./troubleshooting/connection.md)
2. [성능 문제](./troubleshooting/performance.md)
3. [보안 문제](./troubleshooting/security.md)

### 로그 분석
```bash
# 에러 로그 확인
tail -f /var/log/llm_agent/error.log

# 액세스 로그 확인
tail -f /var/log/llm_agent/access.log
``` 