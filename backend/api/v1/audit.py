"""
DataFlowX Audit Trail Endpoints
"""

from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.deps import get_active_workspace_id, get_async_db, get_current_user
from backend.database.models import User
from backend.schemas.common import PaginatedResponse, PaginationParams
from backend.schemas.monitoring import AuditLogOut
from backend.services.audit_service import AuditService

router = APIRouter(prefix="/audit", tags=["Audit & Governance"])


@router.get("/logs", response_model=PaginatedResponse[AuditLogOut])
async def list_audit_logs(
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size, search=search)
    logs, total = await AuditService.list_audit_logs(session, workspace_id, params)
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    return PaginatedResponse(
        items=[
            AuditLogOut(
                id=l.id,
                organization_id=l.organization_id,
                workspace_id=l.workspace_id,
                actor_id=l.actor_id,
                actor_email=l.actor_email,
                action=l.action,
                resource_type=l.resource_type,
                resource_id=l.resource_id,
                ip_address=l.ip_address,
                old_values=l.old_values_json,
                new_values=l.new_values_json,
                timestamp=l.timestamp
            )
            for l in logs
        ],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=(page < total_pages),
        has_prev=(page > 1)
    )
