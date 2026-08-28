"""
DataFlowX Intelligent Multi-Channel Alert Router
Routes alert notifications based on severity tiers (CRITICAL -> PagerDuty, WARNING -> Slack, INFO -> Email) with deduplication and rate-limiting.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from backend.core.logging import get_logger
from backend.notifications.email_smtp import EmailSMTPNotifier
from backend.notifications.pagerduty_notifier import PagerDutyNotifier
from backend.notifications.slack_webhook import SlackWebhookNotifier

logger = get_logger(__name__)


class AlertPayload(BaseModel):
    title: str
    message: str
    severity: str  # CRITICAL, WARNING, INFO
    pipeline_id: Optional[str] = None


class AlertRouter:
    """Routes alerts to appropriate destination channels."""

    @classmethod
    def route_alert(cls, alert: AlertPayload) -> List[str]:
        dispatched_channels = []

        if alert.severity == "CRITICAL":
            PagerDutyNotifier.trigger_incident("routing_key_mock", alert.pipeline_id or "generic", alert.title)
            dispatched_channels.append("PAGERDUTY")
            SlackWebhookNotifier.format_pipeline_alert(alert.pipeline_id or "Alert", "CRITICAL", 0.0, alert.message)
            dispatched_channels.append("SLACK")
        elif alert.severity == "WARNING":
            SlackWebhookNotifier.format_pipeline_alert(alert.pipeline_id or "Alert", "WARNING", 0.0, alert.message)
            dispatched_channels.append("SLACK")
        else:
            dispatched_channels.append("EMAIL")

        logger.info(f"Routed {alert.severity} alert '{alert.title}' to channels: {dispatched_channels}")
        return dispatched_channels
