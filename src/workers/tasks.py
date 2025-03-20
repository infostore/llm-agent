"""작업자 태스크들을 정의합니다."""

import logging
from typing import Any, Dict, Optional

from celery import Celery
from celery.utils.log import get_task_logger

from core.settings import settings
from queue.rabbitmq import RabbitMQPublisher, RabbitMQConsumer
from search.elasticsearch import ElasticsearchClient
from utils.security import sanitize_input

# Celery 앱 초기화
celery_app = Celery(
    "llm_agent",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

# 로거 설정
logger = get_task_logger(__name__)


@celery_app.task(
    name="process_message",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
    """메시지를 처리하는 태스크입니다.

    Args:
        message: 처리할 메시지

    Returns:
        처리 결과
    """
    try:
        # 메시지 정제
        sanitized_message = {
            k: sanitize_input(v) if isinstance(v, str) else v
            for k, v in message.items()
        }

        # 메시지 처리 로직
        result = {
            "status": "success",
            "message": "메시지가 성공적으로 처리되었습니다.",
            "data": sanitized_message,
        }

        return result

    except Exception as exc:
        logger.error(f"메시지 처리 중 오류 발생: {exc}")
        self.retry(exc=exc)


@celery_app.task(
    name="index_document",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def index_document(
    self,
    index: str,
    document: Dict[str, Any],
    document_id: Optional[str] = None,
) -> Dict[str, Any]:
    """문서를 인덱싱하는 태스크입니다.

    Args:
        index: 인덱스 이름
        document: 인덱싱할 문서
        document_id: 문서 ID (선택사항)

    Returns:
        인덱싱 결과
    """
    try:
        # Elasticsearch 클라이언트 초기화
        es_client = ElasticsearchClient()

        # 문서 인덱싱
        result = es_client.index(
            index=index,
            document=document,
            document_id=document_id,
        )

        return {
            "status": "success",
            "message": "문서가 성공적으로 인덱싱되었습니다.",
            "data": result,
        }

    except Exception as exc:
        logger.error(f"문서 인덱싱 중 오류 발생: {exc}")
        self.retry(exc=exc)


@celery_app.task(
    name="publish_message",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def publish_message(
    self,
    exchange: str,
    routing_key: str,
    message: Dict[str, Any],
) -> Dict[str, Any]:
    """메시지를 발행하는 태스크입니다.

    Args:
        exchange: 교환소 이름
        routing_key: 라우팅 키
        message: 발행할 메시지

    Returns:
        발행 결과
    """
    try:
        # RabbitMQ 발행자 초기화
        publisher = RabbitMQPublisher()

        # 메시지 발행
        result = publisher.publish(
            exchange=exchange,
            routing_key=routing_key,
            message=message,
        )

        return {
            "status": "success",
            "message": "메시지가 성공적으로 발행되었습니다.",
            "data": result,
        }

    except Exception as exc:
        logger.error(f"메시지 발행 중 오류 발생: {exc}")
        self.retry(exc=exc)


@celery_app.task(
    name="consume_message",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def consume_message(
    self,
    queue: str,
    callback: str,
) -> Dict[str, Any]:
    """메시지를 소비하는 태스크입니다.

    Args:
        queue: 큐 이름
        callback: 콜백 함수 이름

    Returns:
        소비 결과
    """
    try:
        # RabbitMQ 소비자 초기화
        consumer = RabbitMQConsumer()

        # 메시지 소비
        result = consumer.consume(
            queue=queue,
            callback=callback,
        )

        return {
            "status": "success",
            "message": "메시지가 성공적으로 소비되었습니다.",
            "data": result,
        }

    except Exception as exc:
        logger.error(f"메시지 소비 중 오류 발생: {exc}")
        self.retry(exc=exc)
