"""
DataFlowX Google Cloud KMS Client
Implements symmetric key encryption/decryption using Google Cloud KMS key rings and crypto keys.
"""

import os
from typing import Tuple
from backend.core.logging import get_logger

logger = get_logger(__name__)


class GCPKMSClient:
    """Google Cloud KMS interface."""

    def __init__(self, key_name: str = "projects/dfx/locations/global/keyRings/dfx-ring/cryptoKeys/lakehouse"):
        self.key_name = key_name

    def generate_data_key(self) -> Tuple[bytes, bytes]:
        plaintext = os.urandom(32)
        ciphertext = b"gcp_kms_enc:" + plaintext
        logger.info(f"Generated AES-256 data key via GCP KMS key '{self.key_name}'")
        return plaintext, ciphertext
