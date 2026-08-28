"""
DataFlowX Webhook Endpoint Registry & Security Manager
Registers inbound webhook trigger URLs, provisions per-endpoint HMAC secrets, and tracks invocation analytics.
"""

import secrets
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class WebhookEndpoint(BaseModel):
    webhook_id: str
    target_pipeline_id: str
    path: str
    hmac_secret: str
    enabled: bool = True
    invocation_count: int = 0


class WebhookRegistry:
    """Manages active webhook triggers."""

    def __init__(self):
        self._endpoints: Dict[str, WebhookEndpoint] = {}

    def register_endpoint(self, target_pipeline_id: str) -> WebhookEndpoint:
        wh_id = f"wh_{secrets.token_hex(6)}"
        secret = secrets.token_hex(24)
        endpoint = WebhookEndpoint(
            webhook_id=wh_id,
            target_pipeline_id=target_pipeline_id,
            path=f"/api/v1/webhooks/incoming/{wh_id}",
            hmac_secret=secret
        )
        self._endpoints[wh_id] = endpoint
        logger.info(f"Registered webhook endpoint '{wh_id}' for pipeline '{target_pipeline_id}'")
        return endpoint

    def get_endpoint(self, webhook_id: str) -> Optional[WebhookEndpoint]:
        return self._endpoints.get(webhook_id)
