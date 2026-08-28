"""
DataFlowX JWT Token Management
Handles generation, signing, decoding, and validation of JWT Access and Refresh tokens.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
try:
    import jwt
    from jwt.exceptions import PyJWTError as JWTError
except ImportError:
    from jose import JWTError, jwt
from pydantic import BaseModel
from backend.core.config import settings


class TokenPayload(BaseModel):
    """Decoded JWT payload structure."""
    sub: str  # User ID
    email: str
    username: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    roles: List[str] = []
    permissions: List[str] = []
    type: str = "access"  # 'access' or 'refresh'
    exp: Optional[int] = None
    iat: Optional[int] = None
    jti: Optional[str] = None


class TokenResponse(BaseModel):
    """API token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # Seconds


def create_access_token(
    user_id: str,
    email: str,
    username: str,
    roles: Optional[List[str]] = None,
    permissions: Optional[List[str]] = None,
    organization_id: Optional[str] = None,
    workspace_id: Optional[str] = None,
    expires_delta: Optional[timedelta] = None,
    custom_claims: Optional[Dict[str, Any]] = None,
) -> str:
    """Create a signed JWT access token."""
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode: Dict[str, Any] = {
        "sub": str(user_id),
        "email": email,
        "username": username,
        "organization_id": str(organization_id) if organization_id else None,
        "workspace_id": str(workspace_id) if workspace_id else None,
        "roles": roles or [],
        "permissions": permissions or [],
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    if custom_claims:
        to_encode.update(custom_claims)

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    user_id: str,
    email: str,
    username: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a signed JWT refresh token."""
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode: Dict[str, Any] = {
        "sub": str(user_id),
        "email": email,
        "username": username,
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenPayload:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return TokenPayload(**payload)
    except JWTError as exc:
        raise ValueError(f"Invalid or expired token: {str(exc)}") from exc
