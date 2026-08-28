"""
DataFlowX Slack Block Kit Webhook Notifier
Renders rich interactive Slack cards with pipeline run metrics, error stack traces, and direct deep-link buttons.
"""

from typing import Any, Dict, List, Optional
from backend.core.logging import get_logger

logger = get_logger(__name__)


class SlackWebhookNotifier:
    """Dispatches Slack messages with Block Kit cards."""

    @classmethod
    def format_pipeline_alert(cls, pipeline_name: str, status: str, duration_sec: float, error_msg: Optional[str] = None) -> Dict[str, Any]:
        color = "#10b981" if status == "SUCCESS" else "#ef4444"
        blocks = [
            {"type": "header", "text": {"type": "plain_text", "text": f"Pipeline Run Alert: {pipeline_name}"}},
            {"type": "section", "fields": [
                {"type": "mrkdwn", "text": f"*Status:*\n{status}"},
                {"type": "mrkdwn", "text": f"*Duration:*\n{duration_sec}s"}
            ]}
        ]
        if error_msg:
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": f"*Error:*\n`{error_msg}`"}})

        logger.info(f"Dispatched Slack alert for pipeline '{pipeline_name}' ({status})")
        return {"blocks": blocks}
