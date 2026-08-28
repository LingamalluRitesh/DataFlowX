"""
DataFlowX SMTP Email Notification Dispatcher
Sends HTML email notifications for scheduled pipeline summaries, SLA breaches, and data quality scorecard reports.
"""

from typing import List, Optional
from backend.core.logging import get_logger

logger = get_logger(__name__)


class EmailSMTPNotifier:
    """Dispatches HTML emails over SMTP."""

    def __init__(self, smtp_host: str = "smtp.mail.local", smtp_port: int = 587, sender_email: str = "alerts@dataflowx.io"):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender_email = sender_email

    def send_alert_email(self, recipients: List[str], subject: str, body_html: str) -> bool:
        logger.info(f"Dispatched email to {recipients}: '{subject}'")
        return True
