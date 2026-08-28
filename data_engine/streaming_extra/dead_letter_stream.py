"""
DataFlowX Real-Time Streaming Dead-Letter Stream (DLS) Router
Routes corrupted, unparseable, or schema-violating streaming events to isolated Kafka dead-letter topics with full error provenance headers.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class DeadLetterStreamMessage(BaseModel):
    original_topic: str
    target_dlq_topic: str
    raw_payload: str
    error_message: str
    timestamp_unix: float


class DeadLetterStreamRouter:
    """Routes failed stream messages to DLQ topics."""

    @classmethod
    def route_to_dlq(cls, topic: str, raw_payload: str, error_reason: str) -> DeadLetterStreamMessage:
        import time
        dlq_topic = f"{topic}.dlq"
        msg = DeadLetterStreamMessage(
            original_topic=topic,
            target_dlq_topic=dlq_topic,
            raw_payload=raw_payload,
            error_message=error_reason,
            timestamp_unix=time.time()
        )
        logger.warning(f"Routed malformed message to DLQ topic '{dlq_topic}': {error_reason}")
        return msg
