"""
DataFlowX Authentication Pydantic Schemas
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    """Payload for creating a new user account."""
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    full_name: Optional[str] = Field(default=None, max_length=150)
    organization_name: Optional[str] = Field(default=None, description="Initial organization name to create")


class UserLogin(BaseModel):
    """Payload for logging into the platform."""
    username_or_email: str
    password: str


class RefreshTokenRequest(BaseModel):
    """Payload for refreshing an expired access token."""
    refresh_token: str


class TokenResponse(BaseModel):
    """Access and refresh token output schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserSessionInfo"


class UserSessionInfo(BaseModel):
    """Basic user details embedded in auth responses."""
    id: str
    email: str
    username: str
    full_name: Optional[str] = None
    is_superuser: bool
    is_active: bool
    current_organization_id: Optional[str] = None
    current_workspace_id: Optional[str] = None
    roles: List[str] = []
    permissions: List[str] = []

    model_config = ConfigDict(from_attributes=True)


class PasswordResetRequest(BaseModel):
    """Initiate password reset flow."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Confirm password reset with secure token."""
    token: str
    new_password: str = Field(min_length=8)


class ChangePassword(BaseModel):
    """Change current password while authenticated."""
    current_password: str
    new_password: str = Field(min_length=8)


class UserProfileUpdate(BaseModel):
    """Update profile information."""
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
