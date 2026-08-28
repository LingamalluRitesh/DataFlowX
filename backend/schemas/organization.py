"""
DataFlowX Organization, Workspace & Team Schemas
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class WorkspaceBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    slug: Optional[str] = None
    description: Optional[str] = None
    settings: Optional[dict] = Field(default_factory=dict)


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    settings: Optional[dict] = None


class WorkspaceOut(WorkspaceBase):
    id: str
    organization_id: str
    slug: str
    is_default: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkspaceMemberOut(BaseModel):
    id: str
    workspace_id: str
    user_id: str
    role_name: str
    status: str
    joined_at: datetime
    user_email: Optional[str] = None
    user_full_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class WorkspaceInvitationCreate(BaseModel):
    email: EmailStr
    role_name: str = "data_engineer"


class WorkspaceInvitationOut(BaseModel):
    id: str
    workspace_id: str
    email: str
    role_name: str
    status: str
    expires_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrganizationBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    slug: Optional[str] = None
    logo_url: Optional[str] = None
    plan: str = "enterprise"
    settings: Optional[dict] = Field(default_factory=dict)


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    settings: Optional[dict] = None


class OrganizationOut(OrganizationBase):
    id: str
    slug: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    workspaces: List[WorkspaceOut] = []

    model_config = ConfigDict(from_attributes=True)


class TeamCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = None


class TeamOut(BaseModel):
    id: str
    organization_id: str
    name: str
    description: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
