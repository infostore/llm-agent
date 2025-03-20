"""이벤트 시스템의 기본 클래스들을 정의합니다."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class Event(BaseModel):
    """이벤트 기본 모델입니다."""

    event_id: str
    event_type: str
    timestamp: datetime
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


class EventPublisher(ABC):
    """이벤트 발행자 기본 클래스입니다."""

    @abstractmethod
    async def publish(self, event: Event) -> None:
        """이벤트를 발행합니다.

        Args:
            event: 발행할 이벤트
        """
        pass


class EventHandler(ABC):
    """이벤트 핸들러 기본 클래스입니다."""

    @abstractmethod
    async def handle(self, event: Event) -> None:
        """이벤트를 처리합니다.

        Args:
            event: 처리할 이벤트
        """
        pass
