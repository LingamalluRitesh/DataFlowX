"""
Column-Level Dynamic Data Masking & RBAC Policy Engine.
Enforces PII redaction, tokenization, email obfuscation, and financial data masking on lakehouse query scans.
"""

from typing import Dict, List, Any, Optional, Set
from enum import Enum
import hashlib


class MaskingStrategy(str, Enum):
    FULL_REDACT = "FULL_REDACT"
    HASH_SHA256 = "HASH_SHA256"
    EMAIL_OBFUSCATE = "EMAIL_OBFUSCATE"
    CREDIT_CARD_PARTIAL = "CREDIT_CARD_PARTIAL"
    NULLIFY = "NULLIFY"


class ColumnMaskingEngine:
    """Applies role-based masking rules to tabular records."""

    def __init__(self):
        # column -> role -> strategy
        self.policy_rules: Dict[str, Dict[str, MaskingStrategy]] = {}
        self.exempt_roles: Set[str] = {"SUPERADMIN", "COMPLIANCE_OFFICER"}

    def add_masking_rule(self, column: str, role: str, strategy: MaskingStrategy) -> None:
        if column not in self.policy_rules:
            self.policy_rules[column] = {}
        self.policy_rules[column][role] = strategy

    def _apply_mask(self, value: Any, strategy: MaskingStrategy) -> Any:
        if value is None:
            return None

        val_str = str(value)
        if strategy == MaskingStrategy.NULLIFY:
            return None
        elif strategy == MaskingStrategy.FULL_REDACT:
            return "******"
        elif strategy == MaskingStrategy.HASH_SHA256:
            return hashlib.sha256(val_str.encode("utf-8")).hexdigest()
        elif strategy == MaskingStrategy.EMAIL_OBFUSCATE:
            if "@" in val_str:
                user, domain = val_str.split("@", 1)
                masked_user = user[0] + "***" + (user[-1] if len(user) > 1 else "")
                return f"{masked_user}@{domain}"
            return "******@***.com"
        elif strategy == MaskingStrategy.CREDIT_CARD_PARTIAL:
            digits = "".join(filter(str.isdigit, val_str))
            if len(digits) >= 4:
                return f"****-****-****-{digits[-4:]}"
            return "****-****-****-****"
        return value

    def mask_row(self, row: Dict[str, Any], user_role: str) -> Dict[str, Any]:
        if user_role.upper() in self.exempt_roles:
            return dict(row)

        masked = dict(row)
        for col, strategies in self.policy_rules.items():
            if col in masked:
                strategy = strategies.get(user_role.upper(), strategies.get("DEFAULT"))
                if strategy:
                    masked[col] = self._apply_mask(masked[col], strategy)
        return masked
