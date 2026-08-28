"""
DataFlowX Multi-Tenant Architecture Models
Provides Organizations, Workspaces, Teams, Memberships, and Invitations.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, JSON as JSONB, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base
from backend.database.models.base import SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Organization(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Top-level tenant organization."""
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    plan: Mapped[str] = mapped_column(String(50), default="enterprise", nullable=False)  # free, pro, enterprise
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    settings: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)

    # Relationships
    workspaces: Mapped[List["Workspace"]] = relationship("Workspace", back_populates="organization", cascade="all, delete-orphan")
    teams: Mapped[List["Team"]] = relationship("Team", back_populates="organization", cascade="all, delete-orphan")


class Workspace(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Isolated project workspace within an Organization."""
    __tablename__ = "workspaces"
    __table_args__ = (UniqueConstraint("organization_id", "slug", name="uq_org_workspace_slug"),)

    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    settings: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="workspaces")
    members: Mapped[List["WorkspaceMember"]] = relationship("WorkspaceMember", back_populates="workspace", cascade="all, delete-orphan")
    invitations: Mapped[List["WorkspaceInvitation"]] = relationship("WorkspaceInvitation", back_populates="workspace", cascade="all, delete-orphan")


class WorkspaceMember(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Junction mapping users to workspaces with specific roles."""
    __tablename__ = "workspace_members"
    __table_args__ = (UniqueConstraint("workspace_id", "user_id", name="uq_workspace_user"),)

    workspace_id: Mapped[str] = mapped_column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_name: Mapped[str] = mapped_column(String(50), default="data_engineer", nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)  # active, suspended

    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="members")
    user: Mapped["User"] = relationship("User")


class WorkspaceInvitation(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Pending user invitations to join a workspace."""
    __tablename__ = "workspace_invitations"

    workspace_id: Mapped[str] = mapped_column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    role_name: Mapped[str] = mapped_column(String(50), default="data_engineer", nullable=False)
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)  # pending, accepted, expired, revoked
    invited_by_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="invitations")


class Team(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Team grouping within an Organization."""
    __tablename__ = "teams"
    __table_args__ = (UniqueConstraint("organization_id", "name", name="uq_org_team_name"),)

    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="teams")
    members: Mapped[List["TeamMember"]] = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")


class TeamMember(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Team membership."""
    __tablename__ = "team_members"
    __table_args__ = (UniqueConstraint("team_id", "user_id", name="uq_team_user"),)

    team_id: Mapped[str] = mapped_column(String(36), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(50), default="member", nullable=False)

    team: Mapped["Team"] = relationship("Team", back_populates="members")
    user: Mapped["User"] = relationship("User")
