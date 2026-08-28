"""
DataFlowX SQLAlchemy Base Model & Common Mixins
Provides UUID primary keys, timestamp tracking, soft deletion, and multi-tenant isolation.
"""

from datetime import datetime, timezone
from typing import Optional
import uuid
from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from backend.core.database import Base


def generate_uuid() -> str:
    """Generate a standard UUID4 string."""
    return str(uuid.uuid4())


def utc_now() -> datetime:
    """Return current timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


class UUIDPrimaryKeyMixin:
    """Provides a UUID string primary key."""
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
        index=True
    )


class TimestampMixin:
    """Tracks resource creation and last updated timestamps."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False
    )


class SoftDeleteMixin:
    """Provides soft-deletion state tracking."""
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def soft_delete(self) -> None:
        self.is_deleted = True
        self.deleted_at = utc_now()

    def restore(self) -> None:
        self.is_deleted = False
        self.deleted_at = None


class TenantMixin:
    """Enforces multi-tenant organization and workspace isolation."""
    organization_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    workspace_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
