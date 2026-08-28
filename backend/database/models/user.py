"""
DataFlowX User, Role, Permission & Authentication Models
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, JSON as JSONB, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base
from backend.database.models.base import SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin, generate_uuid


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Platform user account."""
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    extra_metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)

    # Relationships
    roles: Mapped[List["UserRole"]] = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    api_keys: Mapped[List["ApiKey"]] = relationship("ApiKey", back_populates="user", cascade="all, delete-orphan")
    sessions: Mapped[List["UserSession"]] = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")


class Role(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Configurable system and organization RBAC role."""
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_system_role: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    organization_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True)

    # Relationships
    permissions: Mapped[List["RolePermission"]] = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")
    user_assignments: Mapped[List["UserRole"]] = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")


class Permission(Base, UUIDPrimaryKeyMixin):
    """Granular platform action permission."""
    __tablename__ = "permissions"

    code: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    module: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # pipelines, sources, datasets, etc.

    roles: Mapped[List["RolePermission"]] = relationship("RolePermission", back_populates="permission", cascade="all, delete-orphan")


class RolePermission(Base, UUIDPrimaryKeyMixin):
    """Many-to-many junction between Role and Permission."""
    __tablename__ = "role_permissions"
    __table_args__ = (UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),)

    role_id: Mapped[str] = mapped_column(String(36), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, index=True)
    permission_id: Mapped[str] = mapped_column(String(36), ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False, index=True)

    role: Mapped["Role"] = relationship("Role", back_populates="permissions")
    permission: Mapped["Permission"] = relationship("Permission", back_populates="roles")


class UserRole(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Assignment of Role to User within an Organization or Workspace."""
    __tablename__ = "user_roles"
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", "organization_id", "workspace_id", name="uq_user_role_assignment"),
    )

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id: Mapped[str] = mapped_column(String(36), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True, index=True)
    workspace_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=True, index=True)

    user: Mapped["User"] = relationship("User", back_populates="roles")
    role: Mapped["Role"] = relationship("Role", back_populates="user_assignments")


class UserSession(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Tracks active user login sessions and refresh tokens."""
    __tablename__ = "user_sessions"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="sessions")


class PasswordReset(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Temporary tokens for forgotten password recovery."""
    __tablename__ = "password_resets"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class ApiKey(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Programmable API keys for automated integrations."""
    __tablename__ = "api_keys"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    key_hash: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    prefix: Mapped[str] = mapped_column(String(16), nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="api_keys")
