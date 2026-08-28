"""
Unit Tests: Security, Encryption Vault, JWT & Passwords
"""

import pytest
from backend.core.encryption import CredentialVault, vault
from backend.core.jwt import create_access_token, create_refresh_token, decode_token
from backend.core.security import get_password_hash, verify_password


def test_password_hashing():
    raw = "SuperSecretP@ssw0rd2026!"
    hashed = get_password_hash(raw)
    assert hashed != raw
    assert verify_password(raw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_credential_vault_encryption_decryption():
    test_vault = CredentialVault()
    secret_payload = {
        "host": "db.prod.internal",
        "username": "data_admin",
        "password": "MasterDBPassword!@#123",
        "api_key": "sk-dfx-9876543210"
    }

    encrypted_blob = test_vault.encrypt_dict(secret_payload)
    assert isinstance(encrypted_blob, str)
    assert "MasterDBPassword" not in encrypted_blob

    decrypted_payload = test_vault.decrypt_dict(encrypted_blob)
    assert decrypted_payload == secret_payload


def test_jwt_token_issuance_and_decoding():
    user_id = "usr_test_123"
    email = "engineer@dataflowx.io"
    roles = ["data_engineer"]
    permissions = ["pipeline:read", "pipeline:write"]

    token = create_access_token(
        user_id=user_id,
        email=email,
        username="engineer",
        roles=roles,
        permissions=permissions,
        workspace_id="ws_default"
    )

    payload = decode_token(token)
    assert payload.sub == user_id
    assert payload.email == email
    assert payload.roles == roles
    assert payload.permissions == permissions
    assert payload.workspace_id == "ws_default"
    assert payload.type == "access"
