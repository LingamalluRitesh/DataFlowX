"""
DataFlowX Workflow Sensors Service
"""

from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exceptions import NotFoundError
from backend.core.logging import get_logger
from backend.database.models.orchestration_extra import WorkflowSensorModel
from backend.schemas.orchestration_extra import WorkflowSensorCreate

logger = get_logger(__name__)


class SensorService:
    """Service for managing external sensors."""

    @staticmethod
    async def create_sensor(db: AsyncSession, workspace_id: str, data: WorkflowSensorCreate) -> WorkflowSensorModel:
        sensor = WorkflowSensorModel(
            workspace_id=workspace_id,
            name=data.name,
            sensor_type=data.sensor_type,
            config=data.config,
            timeout_seconds=data.timeout_seconds,
            poke_interval_seconds=data.poke_interval_seconds,
            is_active=data.is_active
        )
        db.add(sensor)
        await db.commit()
        await db.refresh(sensor)
        logger.info(f"Created Sensor '{sensor.name}' (id={sensor.id}, type={sensor.sensor_type})")
        return sensor

    @staticmethod
    async def list_sensors(db: AsyncSession, workspace_id: str) -> List[WorkflowSensorModel]:
        stmt = select(WorkflowSensorModel).where(WorkflowSensorModel.workspace_id == workspace_id).order_by(WorkflowSensorModel.created_at.desc())
        result = await db.execute(stmt)
        return list(result.scalars().all())
