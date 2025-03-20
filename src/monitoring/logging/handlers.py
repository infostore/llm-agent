"""로깅 핸들러를 구현합니다."""

import logging
import sys
from typing import Optional

from prometheus_client import Counter, Histogram

# 로그 레벨별 카운터
LOG_COUNTER = Counter(
    "log_messages_total",
    "로그 메시지 수",
    ["level", "module", "function"],
)

# 로그 처리 시간
LOG_PROCESSING_TIME = Histogram(
    "log_processing_seconds",
    "로그 처리 시간",
    ["level"],
    buckets=[0.001, 0.01, 0.1, 0.5, 1.0],
)


class PrometheusHandler(logging.Handler):
    """Prometheus 메트릭을 기록하는 로깅 핸들러입니다."""

    def emit(self, record: logging.LogRecord) -> None:
        """로그 레코드를 처리합니다.

        Args:
            record: 로그 레코드
        """
        try:
            with LOG_PROCESSING_TIME.labels(level=record.levelname).time():
                LOG_COUNTER.labels(
                    level=record.levelname,
                    module=record.module,
                    function=record.funcName,
                ).inc()
        except Exception:
            self.handleError(record)


class JSONHandler(logging.Handler):
    """JSON 형식으로 로그를 출력하는 핸들러입니다."""

    def emit(self, record: logging.LogRecord) -> None:
        """로그 레코드를 처리합니다.

        Args:
            record: 로그 레코드
        """
        try:
            log_entry = {
                "timestamp": self.format(record),
                "level": record.levelname,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
            }
            if hasattr(record, "extra"):
                log_entry.update(record.extra)
            print(log_entry, file=sys.stdout)
        except Exception:
            self.handleError(record)
