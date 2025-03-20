"""이벤트 핸들러 기본 클래스를 구현합니다."""

from typing import Dict, Type

from ..base import Event, EventHandler


class EventHandlerRegistry:
    """이벤트 핸들러 레지스트리입니다."""

    def __init__(self):
        """이벤트 핸들러 레지스트리를 초기화합니다."""
        self._handlers: Dict[str, Type[EventHandler]] = {}

    def register(self, event_type: str, handler: Type[EventHandler]) -> None:
        """이벤트 핸들러를 등록합니다.

        Args:
            event_type: 이벤트 타입
            handler: 이벤트 핸들러 클래스
        """
        self._handlers[event_type] = handler

    def get_handler(self, event_type: str) -> Type[EventHandler]:
        """이벤트 핸들러를 가져옵니다.

        Args:
            event_type: 이벤트 타입

        Returns:
            Type[EventHandler]: 이벤트 핸들러 클래스

        Raises:
            KeyError: 핸들러가 등록되지 않은 경우
        """
        if event_type not in self._handlers:
            raise KeyError(
                f"이벤트 타입 '{event_type}'에 대한 핸들러가 등록되지 않았습니다."
            )
        return self._handlers[event_type]

    def has_handler(self, event_type: str) -> bool:
        """이벤트 핸들러가 등록되어 있는지 확인합니다.

        Args:
            event_type: 이벤트 타입

        Returns:
            bool: 핸들러 존재 여부
        """
        return event_type in self._handlers


# 전역 이벤트 핸들러 레지스트리
event_handler_registry = EventHandlerRegistry()


def register_event_handler(event_type: str):
    """이벤트 핸들러 데코레이터입니다.

    Args:
        event_type: 이벤트 타입
    """

    def decorator(handler: Type[EventHandler]):
        event_handler_registry.register(event_type, handler)
        return handler

    return decorator
