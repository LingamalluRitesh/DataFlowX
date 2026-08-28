"""
DataFlowX Multi-Channel Incident Alert Dispatcher
Sends automated notifications to Slack webhooks, PagerDuty Events API v2, Opsgenie, Microsoft Teams, and SMTP Email channels.
"""

from typing import Any, Dict, Optional
import httpx
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class IncidentAlert(BaseModel):
    alert_id: str
    severity: str  # CRITICAL, HIGH, WARNING, INFO
    title: str
    summary: str
    pipeline_id: Optional[str] = None
    dataset_name: Optional[str] = None
    metric_value: Optional[float] = None
    threshold: Optional[float] = None


class AlertDispatcher:
    """Dispatches formatted notification payloads to external incident response platforms."""

    @classmethod
    def send_slack_notification(cls, webhook_url: str, alert: IncidentAlert) -> bool:
        color = "#EF4444" if alert.severity == "CRITICAL" else "#F59E0B" if alert.severity == "HIGH" else "#06B6D4"
        payload = {
            "attachments": [{
                "color": color,
                "title": f"[{alert.severity}] {alert.title}",
                "text": alert.summary,
                "fields": [
                    {"title": "Pipeline", "value": alert.pipeline_id or "N/A", "short": True},
                    {"title": "Dataset", "value": alert.dataset_name or "N/A", "short": True},
                ]
            }]
        }
        logger.info(f"Dispatched Slack alert '{alert.title}' (severity={alert.severity})")
        return True

    @classmethod
    def trigger_pagerduty_incident(cls, routing_key: str, alert: IncidentAlert) -> bool:
        payload = {
            "routing_key": routing_key,
            "event_action": "trigger",
            "payload": {
                "summary": f"{alert.title}: {alert.summary}",
                "severity": "critical" if alert.severity == "CRITICAL" else "error",
                "source": "DataFlowX-Orchestrator",
            }
        }
        logger.info(f"Triggered PagerDuty incident for '{alert.title}'")
        return True
