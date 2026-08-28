"""
Backfill Jobs REST API Endpoints
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.v1.deps import get_current_user
from backend.core.database import get_async_db
from backend.database.models.user import User
from backend.schemas.orchestration_extra import BackfillCreate, BackfillOut
from backend.services.backfill_service import BackfillService

router = APIRouter(prefix="/backfills", tags=["Historical Backfills"])


@router.get("", response_model=List[BackfillOut])
async def list_backfills(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """List historical backfill jobs in current workspace."""
    workspace_id = current_user.workspaces[0].workspace_id if current_user.workspaces else "ws_default"
    return await BackfillService.list_backfills(db, workspace_id)


@router.post("", response_model=BackfillOut, status_code=status.HTTP_201_CREATED)
async def create_backfill(
    payload: BackfillCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Trigger a date-partitioned historical backfill job."""
    workspace_id = current_user.workspaces[0].workspace_id if current_user.workspaces else "ws_default"
    return await BackfillService.create_backfill(db, workspace_id, payload)


@router.get("/{backfill_id}", response_model=BackfillOut)
async def get_backfill(
    backfill_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve details and partition status of specific backfill."""
    workspace_id = current_user.workspaces[0].workspace_id if current_user.workspaces else "ws_default"
    return await BackfillService.get_backfill_by_id(db, backfill_id, workspace_id)
