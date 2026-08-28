"""
DataFlowX Webhook HMAC-SHA256 Signature Validator
Validates X-Signature-256 HMAC headers and checks timestamp drifts (<300s) to prevent replay attacks on webhook trigger endpoints.
"""

import hmac
import hashlib
import time
from typing import Optional


class WebhookHMACValidator:
    """Validates HMAC signatures."""

    @classmethod
    def verify_signature(cls, secret_key: str, payload_bytes: bytes, received_signature: str, timestamp_str: Optional[str] = None) -> bool:
        if not received_signature:
            return False

        # Verify timestamp drift if provided
        if timestamp_str:
            try:
                req_ts = float(timestamp_str)
                if abs(time.time() - req_ts) > 300.0:  # 5 min window
                    return False
            except ValueError:
                return False

        expected_sig = hmac.new(secret_key.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_sig.lower(), received_signature.lower().replace("sha256=", ""))
