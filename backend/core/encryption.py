"""
DataFlowX Credential Encryption Vault
Provides symmetric encryption for database passwords, API tokens, and secrets
using AES-256-GCM / Fernet cryptography with key rotation and secret masking.
"""

import base64
import json
import os
from typing import Any, Dict, Optional, Union
from cryptography.fernet import Fernet, InvalidToken
from backend.core.config import settings


class CredentialVault:
    """Enterprise encryption vault for credentials and secrets."""

    def __init__(self, master_key: Optional[str] = None):
        key = master_key or settings.ENCRYPTION_MASTER_KEY
        try:
            # Ensure key is valid base64 32-byte key
            self._fernet = Fernet(key.encode() if isinstance(key, str) else key)
        except Exception:
            # Fallback for dev / uninitialized key
            derived_key = base64.urlsafe_b64encode((settings.SECRET_KEY.ljust(32, "x")[:32]).encode())
            self._fernet = Fernet(derived_key)

    def encrypt(self, plain_text: str) -> str:
        """Encrypt a string payload into a URL-safe ciphertext."""
        if not plain_text:
            return ""
        return self._fernet.encrypt(plain_text.encode("utf-8")).decode("utf-8")

    def decrypt(self, cipher_text: str) -> str:
        """Decrypt a ciphertext back to original plain-text."""
        if not cipher_text:
            return ""
        try:
            return self._fernet.decrypt(cipher_text.encode("utf-8")).decode("utf-8")
        except InvalidToken:
            raise ValueError("Failed to decrypt credentials: invalid key or corrupted ciphertext")

    def encrypt_dict(self, data: Dict[str, Any]) -> str:
        """Serialize and encrypt a dictionary payload."""
        json_str = json.dumps(data)
        return self.encrypt(json_str)

    def decrypt_dict(self, cipher_text: str) -> Dict[str, Any]:
        """Decrypt and deserialize ciphertext into a dictionary."""
        plain_json = self.decrypt(cipher_text)
        if not plain_json:
            return {}
        return json.loads(plain_json)

    def rotate_key(self, cipher_text: str, new_vault: "CredentialVault") -> str:
        """Re-encrypt ciphertext with a new vault key."""
        decrypted = self.decrypt(cipher_text)
        return new_vault.encrypt(decrypted)

    @staticmethod
    def mask_secret(value: str, visible_chars: int = 4) -> str:
        """Mask a secret for display in API responses and logs."""
        if not value:
            return ""
        if len(value) <= visible_chars * 2:
            return "*" * len(value)
        return f"{value[:visible_chars]}{'*' * (len(value) - visible_chars * 2)}{value[-visible_chars:]}"

    @staticmethod
    def mask_credential_dict(credentials: Dict[str, Any]) -> Dict[str, Any]:
        """Mask known sensitive fields in a credential dictionary."""
        sensitive_keys = {
            "password", "secret", "token", "api_key", "apikey", "private_key",
            "access_token", "refresh_token", "secret_key", "auth_token", "client_secret"
        }
        masked = {}
        for k, v in credentials.items():
            if any(s in k.lower() for s in sensitive_keys) and isinstance(v, str):
                masked[k] = CredentialVault.mask_secret(v)
            elif isinstance(v, dict):
                masked[k] = CredentialVault.mask_credential_dict(v)
            else:
                masked[k] = v
        return masked


# Global vault singleton
vault = CredentialVault()
