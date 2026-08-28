"""
DataFlowX Cryptographic Security & Key Derivation Toolkit
Provides PBKDF2 HMAC-SHA256 password hashing, deterministic HMAC tokenization, and Base64 URL-safe encoding for secure data pipelines.
"""

import base64
import hashlib
import hmac
import os
from typing import Optional
import pandas as pd


class CryptoToolkit:
    """Cryptographic primitives for enterprise pipeline security."""

    @staticmethod
    def compute_hmac_sha256(secret_key: str, message: str) -> str:
        """Compute HMAC-SHA256 signature."""
        key_bytes = secret_key.encode("utf-8")
        msg_bytes = message.encode("utf-8")
        return hmac.new(key_bytes, msg_bytes, hashlib.sha256).hexdigest()

    @staticmethod
    def pbkdf2_hash(password: str, salt: Optional[bytes] = None, iterations: int = 100000) -> str:
        """Derive secure cryptographic key using PBKDF2."""
        s = salt or os.urandom(16)
        derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), s, iterations)
        return f"{base64.b64encode(s).decode('utf-8')}${base64.b64encode(derived).decode('utf-8')}"

    @classmethod
    def apply_hmac_tokenization(cls, df: pd.DataFrame, col: str, secret_key: str, output_col: Optional[str] = None) -> pd.DataFrame:
        if df.empty or col not in df.columns:
            return df
        df = df.copy()
        out = output_col or f"{col}_hmac"
        df[out] = df[col].astype(str).apply(lambda v: cls.compute_hmac_sha256(secret_key, v))
        return df
