"""RabbitMQ 큐 구현을 구현합니다."""

import json
import uuid
from typing import Optional

import aio_pika
from aio_pika import IncomingMessage, Message, Queue, QueueDeclareOk

from .base import Message, QueueConsumer, QueuePublisher

from core.settings import get_settings

settings = get_settings()


class RabbitMQPublisher(QueuePublisher):
    """RabbitMQ 발행자입니다."""

    def __init__(
        self,
        url: Optional[str] = None,
        exchange_name: str = "default",
    ):
        """RabbitMQ 발행자를 초기화합니다.

        Args:
            url: RabbitMQ URL
            exchange_name: 교환소 이름
        """
        self.url = url or settings.RABBITMQ_URL
        self.exchange_name = exchange_name
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.exchange: Optional[aio_pika.Exchange] = None

    async def connect(self) -> None:
        """RabbitMQ에 연결합니다."""
        if not self.connection:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
            self.exchange = await self.channel.declare_exchange(
                self.exchange_name,
                aio_pika.ExchangeType.TOPIC,
            )

    async def disconnect(self) -> None:
        """RabbitMQ 연결을 종료합니다."""
        if self.connection:
            await self.connection.close()
            self.connection = None
            self.channel = None
            self.exchange = None

    async def publish(self, message: Message) -> None:
        """메시지를 발행합니다.

        Args:
            message: 발행할 메시지
        """
        if not self.exchange:
            await self.connect()
            if not self.exchange:
                raise RuntimeError("RabbitMQ 연결에 실패했습니다.")

        message_body = message.model_dump_json()
        await self.exchange.publish(
            Message(
                body=message_body.encode(),
                message_id=str(uuid.uuid4()),
                content_type="application/json",
            ),
            routing_key=message.queue_name,
        )


class RabbitMQConsumer(QueueConsumer):
    """RabbitMQ 소비자입니다."""

    def __init__(
        self,
        url: Optional[str] = None,
        exchange_name: str = "default",
    ):
        """RabbitMQ 소비자를 초기화합니다.

        Args:
            url: RabbitMQ URL
            exchange_name: 교환소 이름
        """
        self.url = url or settings.RABBITMQ_URL
        self.exchange_name = exchange_name
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.exchange: Optional[aio_pika.Exchange] = None
        self.queue: Optional[Queue] = None

    async def connect(self) -> None:
        """RabbitMQ에 연결합니다."""
        if not self.connection:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
            self.exchange = await self.channel.declare_exchange(
                self.exchange_name,
                aio_pika.ExchangeType.TOPIC,
            )

    async def disconnect(self) -> None:
        """RabbitMQ 연결을 종료합니다."""
        if self.connection:
            await self.connection.close()
            self.connection = None
            self.channel = None
            self.exchange = None
            self.queue = None

    async def subscribe(self, queue_name: str) -> None:
        """큐를 구독합니다.

        Args:
            queue_name: 구독할 큐 이름
        """
        if not self.channel:
            await self.connect()
            if not self.channel:
                raise RuntimeError("RabbitMQ 연결에 실패했습니다.")

        self.queue = await self.channel.declare_queue(queue_name)
        await self.queue.bind(self.exchange, routing_key=queue_name)

    async def consume(self, callback: callable) -> None:
        """메시지를 소비합니다.

        Args:
            callback: 메시지 처리 콜백 함수
        """
        if not self.queue:
            raise RuntimeError("먼저 큐를 구독해야 합니다.")

        async def process_message(message: IncomingMessage):
            """메시지를 처리합니다.

            Args:
                message: 수신된 메시지
            """
            async with message.process():
                try:
                    message_data = json.loads(message.body.decode())
                    await callback(Message(**message_data))
                except Exception as e:
                    print(f"메시지 처리 중 오류 발생: {e}")

        await self.queue.consume(process_message)
