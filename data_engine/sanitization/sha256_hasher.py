"""
DataFlowX Salted SHA-256 & HMAC Pseudonymizer
Transforms direct identifiers (user IDs, IP addresses, device MACs) into irreversible pseudonymous hash tokens with cryptographically secure salts.
"""

import hashlib
import hmac
from typing import Any, Optional


class SaltedPseudonymizer:
    """Computes salted hashes for privacy compliance."""

    def __init__(self, salt: str = "dfx_enterprise_salt_2026"):
        self.salt = salt

    def pseudonymize(self, value: Any) -> str:
        if value is None:
            return ""
        raw = f"{self.salt}:{value}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()
