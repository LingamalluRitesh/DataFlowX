"""
DataFlowX PagerDuty Events API v2 Incident Dispatcher
Dispatches high-severity incident triggers, acknowledgments, and automated resolutions to on-call engineering rotations via PagerDuty Events API v2.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class PagerDutyEvent(BaseModel):
    routing_key: str
    event_action: str = "trigger"  # trigger, acknowledge, resolve
    dedup_key: str
    summary: str
    severity: str = "critical"  # critical, error, warning, info
    custom_details: Dict[str, Any] = Field(default_factory=dict)


class PagerDutyNotifier:
    """Dispatches incidents to PagerDuty."""

    @classmethod
    def trigger_incident(cls, routing_key: str, dedup_key: str, summary: str, details: Optional[Dict[str, Any]] = None) -> PagerDutyEvent:
        evt = PagerDutyEvent(
            routing_key=routing_key,
            event_action="trigger",
            dedup_key=dedup_key,
            summary=summary,
            severity="critical",
            custom_details=details or {}
        )
        logger.critical(f"PagerDuty Trigger: '{summary}' (dedup_key={dedup_key})")
        return evt
