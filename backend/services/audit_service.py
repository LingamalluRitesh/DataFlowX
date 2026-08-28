"""
DataFlowX Audit Trail Logging Service
Records and queries security, data access, and resource mutation events.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models import AuditLog
from backend.schemas.common import PaginationParams


class AuditService:
    """Enterprise audit trail recording and search."""

    @staticmethod
    async def record_event(
        session: AsyncSession,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        actor_id: Optional[str] = None,
        actor_email: Optional[str] = None,
        organization_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        log = AuditLog(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            actor_id=actor_id,
            actor_email=actor_email,
            organization_id=organization_id,
            workspace_id=workspace_id,
            ip_address=ip_address,
            user_agent=user_agent,
            old_values_json=old_values,
            new_values_json=new_values,
            metadata_json=metadata or {},
            timestamp=datetime.now(timezone.utc)
        )
        session.add(log)
        await session.commit()
        return log

    @staticmethod
    async def list_audit_logs(
        session: AsyncSession,
        workspace_id: Optional[str],
        params: PaginationParams
    ) -> Tuple[List[AuditLog], int]:
        query = select(AuditLog)
        if workspace_id:
            query = query.where(AuditLog.workspace_id == workspace_id)
        if params.search:
            s = f"%{params.search}%"
            query = query.where(
                (AuditLog.action.ilike(s)) |
                (AuditLog.resource_type.ilike(s)) |
                (AuditLog.actor_email.ilike(s))
            )

        total_stmt = select(func.count()).select_from(query.subquery())
        total = (await session.execute(total_stmt)).scalar() or 0

        query = query.order_by(AuditLog.timestamp.desc()).offset((params.page - 1) * params.page_size).limit(params.page_size)
        items = (await session.execute(query)).scalars().all()
        return list(items), total
