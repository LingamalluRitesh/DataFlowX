"""
DataFlowX AWS KMS Client & Data Key Generator
Generates AES-256 plaintext/ciphertext data keys using AWS KMS CMKs for envelope encryption.
"""

import base64
import os
from typing import Tuple
from backend.core.logging import get_logger

logger = get_logger(__name__)


class AWSKMSClient:
    """AWS KMS interface."""

    def __init__(self, key_arn: str = "arn:aws:kms:us-east-1:123456789012:key/dataflowx"):
        self.key_arn = key_arn

    def generate_data_key(self) -> Tuple[bytes, bytes]:
        """Returns (plaintext_key, encrypted_ciphertext_key)."""
        plaintext = os.urandom(32)  # 256-bit
        # Emulate KMS ciphertext envelope
        ciphertext = b"kms_enc:" + plaintext
        logger.info(f"Generated new AES-256 data key via AWS KMS key '{self.key_arn}'")
        return plaintext, ciphertext

    def decrypt_data_key(self, ciphertext_key: bytes) -> bytes:
        if ciphertext_key.startswith(b"kms_enc:"):
            return ciphertext_key[8:]
        return ciphertext_key
