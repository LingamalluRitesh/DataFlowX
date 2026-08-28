"""
DataFlowX User, Role & Permission Schemas
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class PermissionOut(BaseModel):
    """Permission definition details."""
    id: str
    code: str
    name: str
    description: Optional[str] = None
    module: str

    model_config = ConfigDict(from_attributes=True)


class RoleBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    is_system_role: bool = False


class RoleCreate(RoleBase):
    permission_ids: List[str] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permission_ids: Optional[List[str]] = None


class RoleOut(RoleBase):
    id: str
    organization_id: Optional[str] = None
    created_at: datetime
    permissions: List[PermissionOut] = []

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(min_length=8)
    role_ids: Optional[List[str]] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    avatar_url: Optional[str] = None
    role_ids: Optional[List[str]] = None


class UserOut(UserBase):
    id: str
    is_verified: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApiKeyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    expires_in_days: Optional[int] = Field(default=365)


class ApiKeyOut(BaseModel):
    id: str
    name: str
    prefix: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    is_active: bool
    raw_key: Optional[str] = None  # Only returned on creation

    model_config = ConfigDict(from_attributes=True)
