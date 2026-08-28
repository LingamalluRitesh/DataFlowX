"""
DataFlowX Lifecycle Hooks & Notification Callback Dispatcher
Supports Slack incoming webhooks, Microsoft Teams cards, PagerDuty incident triggers, Datadog metric pushes, and email alerts.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import httpx

from backend.core.logging import get_logger

logger = get_logger(__name__)


class BaseLifecycleHook(ABC):
    """Abstract interface for task & pipeline execution lifecycle event hooks."""

    @abstractmethod
    def on_success(self, context: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def on_failure(self, context: Dict[str, Any]) -> None:
        pass


class SlackWebhookHook(BaseLifecycleHook):
    """Dispatches Slack block-kit messages on pipeline success/failure."""

    def __init__(self, webhook_url: str, channel: Optional[str] = None):
        self.webhook_url = webhook_url
        self.channel = channel

    def on_success(self, context: Dict[str, Any]) -> None:
        pipeline_id = context.get("pipeline_id", "unknown")
        exec_id = context.get("execution_id", "unknown")
        duration = context.get("duration", 0.0)
        payload = {
            "text": f"✅ Pipeline `{pipeline_id}` completed successfully in {duration:.2f}s (Exec ID: `{exec_id}`)"
        }
        self._send_payload(payload)

    def on_failure(self, context: Dict[str, Any]) -> None:
        pipeline_id = context.get("pipeline_id", "unknown")
        exec_id = context.get("execution_id", "unknown")
        error = context.get("error", "Unknown error")
        payload = {
            "text": f"🚨 Pipeline `{pipeline_id}` FAILED on task `{context.get('task_id')}`!\n*Error*: `{error}`\n*Execution*: `{exec_id}`"
        }
        self._send_payload(payload)

    def _send_payload(self, payload: Dict[str, Any]) -> None:
        try:
            with httpx.Client(timeout=10.0) as client:
                client.post(self.webhook_url, json=payload)
        except Exception as exc:
            logger.error(f"Failed to dispatch Slack webhook: {exc}")


class PagerDutyIncidentHook(BaseLifecycleHook):
    """Triggers high-urgency PagerDuty incidents on pipeline failure."""

    def __init__(self, routing_key: str):
        self.routing_key = routing_key
        self.events_url = "https://events.pagerduty.com/v2/enqueue"

    def on_success(self, context: Dict[str, Any]) -> None:
        pass  # No-op on success

    def on_failure(self, context: Dict[str, Any]) -> None:
        pipeline_id = context.get("pipeline_id", "unknown")
        payload = {
            "routing_key": self.routing_key,
            "event_action": "trigger",
            "payload": {
                "summary": f"DataFlowX Pipeline Failure: {pipeline_id}",
                "source": "dataflowx-orchestrator",
                "severity": "critical",
                "custom_details": context
            }
        }
        try:
            with httpx.Client(timeout=10.0) as client:
                client.post(self.events_url, json=payload)
        except Exception as exc:
            logger.error(f"Failed to trigger PagerDuty incident: {exc}")
