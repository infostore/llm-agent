"""큐 시스템의 기본 클래스를 정의합니다."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from pydantic import BaseModel


class Message(BaseModel):
    """메시지 기본 모델입니다."""

    message_id: str
    queue_name: str
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


class QueuePublisher(ABC):
    """큐 발행자 기본 클래스입니다."""

    @abstractmethod
    async def connect(self) -> None:
        """큐 시스템에 연결합니다."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """큐 시스템 연결을 종료합니다."""
        pass

    @abstractmethod
    async def publish(self, message: Message) -> None:
        """메시지를 발행합니다.

        Args:
            message: 발행할 메시지
        """
        pass


class QueueConsumer(ABC):
    """큐 소비자 기본 클래스입니다."""

    @abstractmethod
    async def connect(self) -> None:
        """큐 시스템에 연결합니다."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """큐 시스템 연결을 종료합니다."""
        pass

    @abstractmethod
    async def subscribe(self, queue_name: str) -> None:
        """큐를 구독합니다.

        Args:
            queue_name: 구독할 큐 이름
        """
        pass

    @abstractmethod
    async def consume(self, callback: callable) -> None:
        """메시지를 소비합니다.

        Args:
            callback: 메시지 처리 콜백 함수
        """
        pass
