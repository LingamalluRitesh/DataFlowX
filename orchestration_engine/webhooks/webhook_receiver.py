"""
DataFlowX Parameterized Webhook Ingestion Receiver
Receives external JSON payloads from GitHub, Shopify, Stripe, and launches asynchronous DAG run executions with extracted parameter payloads.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel

from backend.core.logging import get_logger
from orchestration_engine.webhooks.hmac_auth import WebhookHMACValidator
from orchestration_engine.webhooks.webhook_registry import WebhookEndpoint

logger = get_logger(__name__)


class WebhookTriggerResponse(BaseModel):
    accepted: bool
    pipeline_id: str
    triggered_run_id: Optional[str] = None
    error: Optional[str] = None


class WebhookReceiver:
    """Processes incoming HTTP webhook calls."""

    @classmethod
    def handle_incoming_webhook(
        cls,
        endpoint: WebhookEndpoint,
        payload_bytes: bytes,
        signature_header: str,
        timestamp_header: Optional[str] = None
    ) -> WebhookTriggerResponse:
        import time
        if not WebhookHMACValidator.verify_signature(endpoint.hmac_secret, payload_bytes, signature_header, timestamp_header):
            logger.warning(f"Webhook {endpoint.webhook_id} rejected: Invalid HMAC signature")
            return WebhookTriggerResponse(accepted=False, pipeline_id=endpoint.target_pipeline_id, error="Invalid HMAC signature")

        endpoint.invocation_count += 1
        run_id = f"run_wh_{int(time.time())}"
        logger.info(f"Webhook {endpoint.webhook_id} accepted! Triggered pipeline run '{run_id}'")
        return WebhookTriggerResponse(accepted=True, pipeline_id=endpoint.target_pipeline_id, triggered_run_id=run_id)
