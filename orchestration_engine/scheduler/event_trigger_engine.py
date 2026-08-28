"""
DataFlowX Event-Driven Pipeline Trigger Engine
Evaluates cloud storage notifications (S3 ObjectCreated), Kafka topic arrival thresholds, and Webhook payloads to trigger downstream pipeline DAGs with debounce window controls.
"""

from datetime import datetime, timezone
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class EventTriggerRule(BaseModel):
    trigger_id: str
    pipeline_id: str
    event_source: str  # S3_OBJECT_CREATED, KAFKA_MESSAGE, WEBHOOK, DATASET_UPDATE
    pattern_match: str  # e.g., "s3://landing/orders/*.parquet"
    debounce_seconds: int = 30
    is_active: bool = True


class EventTriggerEngine:
    """Debounces and evaluates event triggers before dispatching execution commands."""

    def __init__(self, rules: List[EventTriggerRule]):
        self.rules = rules
        self._last_triggered: Dict[str, float] = {}

    def on_event_received(self, event_source: str, event_payload: Dict[str, Any]) -> List[str]:
        """
        Match incoming event against registered trigger rules.
        Returns list of pipeline_ids to execute.
        """
        now = time.time()
        pipelines_to_run = []

        for rule in self.rules:
            if not rule.is_active or rule.event_source != event_source:
                continue

            last_run = self._last_triggered.get(rule.trigger_id, 0.0)
            if now - last_run < rule.debounce_seconds:
                logger.debug(f"Event trigger '{rule.trigger_id}' debounced ({rule.debounce_seconds}s window)")
                continue

            self._last_triggered[rule.trigger_id] = now
            pipelines_to_run.append(rule.pipeline_id)
            logger.info(f"Trigger '{rule.trigger_id}' matched event on '{event_source}'. Dispatching pipeline '{rule.pipeline_id}'")

        return pipelines_to_run
