"""
Workflow Sensors REST API Endpoints
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.v1.deps import get_current_user
from backend.core.database import get_async_db
from backend.database.models.user import User
from backend.schemas.orchestration_extra import WorkflowSensorCreate, WorkflowSensorOut
from backend.services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["Workflow Sensors"])


@router.get("", response_model=List[WorkflowSensorOut])
async def list_sensors(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """List all configured external sensors."""
    workspace_id = current_user.workspaces[0].workspace_id if current_user.workspaces else "ws_default"
    return await SensorService.list_sensors(db, workspace_id)


@router.post("", response_model=WorkflowSensorOut, status_code=status.HTTP_201_CREATED)
async def create_sensor(
    payload: WorkflowSensorCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Register a new workflow sensor."""
    workspace_id = current_user.workspaces[0].workspace_id if current_user.workspaces else "ws_default"
    return await SensorService.create_sensor(db, workspace_id, payload)
