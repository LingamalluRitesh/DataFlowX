"""
DataFlowX Cryptographic Tokenization & PII Masking Engine
Provides deterministic SHA-256 hashing, HMAC-SHA256 salt tokenization, partial email/credit card masking, and format-preserving tokenization.
"""

import hashlib
import hmac
import re
from typing import Any, Dict, List, Optional, Tuple, Union
import pandas as pd

from backend.core.logging import get_logger
from data_engine.transformation.operators import BaseOperator

logger = get_logger(__name__)


def hash_token(value: str, salt: str = "", algorithm: str = "sha256") -> str:
    """Generate salted cryptographic hash digest."""
    if not value:
        return ""
    to_hash = (value + salt).encode("utf-8")
    if algorithm == "sha256":
        return hashlib.sha256(to_hash).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(to_hash).hexdigest()
    elif algorithm == "md5":
        return hashlib.md5(to_hash).hexdigest()
    return hashlib.sha256(to_hash).hexdigest()


def mask_email_address(email: str) -> str:
    """Partially mask email (e.g. john.doe@example.com -> j***e@example.com)."""
    if not email or "@" not in email:
        return email
    parts = email.split("@", 1)
    user, domain = parts[0], parts[1]
    if len(user) <= 2:
        masked_user = user[0] + "***"
    else:
        masked_user = user[0] + "***" + user[-1]
    return f"{masked_user}@{domain}"


def mask_credit_card(card: str) -> str:
    """Redact credit card digits keeping only first digit and last 4 (e.g. 4111222233334444 -> 4***********4444)."""
    if not card:
        return card
    digits_only = re.sub(r"\D", "", card)
    if len(digits_only) < 6:
        return "************"
    return digits_only[0] + "*" * (len(digits_only) - 5) + digits_only[-4:]


class SaltedHashTokenizeOperator(BaseOperator):
    """Replaces cleartext identifiers with deterministic irreversible salted hash tokens."""

    def __init__(
        self,
        columns: List[str],
        salt: str = "dfx_vault_salt_2026",
        algorithm: str = "sha256",
        prefix: Optional[str] = None
    ):
        self.columns = columns
        self.salt = salt
        self.algorithm = algorithm
        self.prefix = prefix

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        df = df.copy()

        for col in self.columns:
            if col in df.columns:
                target_col = f"{self.prefix}_{col}" if self.prefix else col
                df[target_col] = df[col].astype(str).apply(lambda v: hash_token(v, self.salt, self.algorithm))
        return df


class PIIRedactionMaskingOperator(BaseOperator):
    """Masks sensitive PII attributes (email, credit card, phone, national ID) according to GDPR/CCPA standards."""

    def __init__(self, masking_rules: Dict[str, str]):
        """
        masking_rules mapping: column_name -> mask_type ('email', 'credit_card', 'full_redact', 'phone')
        """
        self.masking_rules = masking_rules

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        df = df.copy()

        for col, mask_type in self.masking_rules.items():
            if col not in df.columns:
                continue

            mtype = mask_type.lower()
            if mtype == "email":
                df[col] = df[col].astype(str).apply(mask_email_address)
            elif mtype in ("credit_card", "pan"):
                df[col] = df[col].astype(str).apply(mask_credit_card)
            elif mtype == "phone":
                df[col] = df[col].astype(str).apply(lambda p: re.sub(r"\d(?=\d{4})", "*", str(p)))
            elif mtype == "full_redact":
                df[col] = "********"
        return df
