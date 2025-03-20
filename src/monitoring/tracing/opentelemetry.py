"""OpenTelemetry 추적 설정을 구현합니다."""

from typing import Optional

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from core.settings import get_settings

settings = get_settings()


def init_tracing(
    service_name: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> None:
    """추적을 초기화합니다.

    Args:
        service_name: 서비스 이름
        endpoint: OpenTelemetry Collector 엔드포인트
    """
    # 리소스 설정
    resource = Resource.create(
        {
            "service.name": service_name or "llm-agent",
        }
    )

    # 트레이서 프로바이더 설정
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # 스팬 익스포터 설정
    exporter = OTLPSpanExporter(
        endpoint=endpoint or settings.OTEL_EXPORTER_OTLP_ENDPOINT,
    )
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)

    # FastAPI 계측
    FastAPIInstrumentor.instrument(
        tracer_provider=provider,
        service_name=service_name or "llm-agent",
    )
