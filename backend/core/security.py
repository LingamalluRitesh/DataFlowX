"""
DataFlowX Security & Cryptography Module
Provides password hashing, verification, API key generation, and token helpers.
"""

import os
import re
import secrets
import string
from typing import Optional, Tuple
from passlib.context import CryptContext

# Configure password hashing scheme with bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    if not plain_password or not hashed_password:
        return False
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Generate a secure bcrypt hash for a password."""
    return pwd_context.hash(password)


def validate_password_strength(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validate password complexity:
    - At least 8 characters
    - Contains at least 1 uppercase letter
    - Contains at least 1 lowercase letter
    - Contains at least 1 number
    - Contains at least 1 special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, None


def generate_secure_token(length: int = 32) -> str:
    """Generate a URL-safe cryptographically secure token."""
    return secrets.token_urlsafe(length)


def generate_api_key(prefix: str = "dfx_live") -> str:
    """Generate a prefixed enterprise API key."""
    random_part = secrets.token_hex(24)
    return f"{prefix}_{random_part}"


def generate_random_password(length: int = 16) -> str:
    """Generate a compliant random password for initialization."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        pwd = "".join(secrets.choice(chars) for _ in range(length))
        valid, _ = validate_password_strength(pwd)
        if valid:
            return pwd
