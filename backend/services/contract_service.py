"""
DataFlowX Data Contract Service
"""

from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exceptions import NotFoundError
from backend.core.logging import get_logger
from backend.database.models.governance import DataContractModel
from backend.schemas.governance import DataContractCreate

logger = get_logger(__name__)


class ContractService:
    """Service for managing producer-consumer schema contracts."""

    @staticmethod
    async def create_contract(db: AsyncSession, workspace_id: str, data: DataContractCreate) -> DataContractModel:
        contract = DataContractModel(
            workspace_id=workspace_id,
            dataset_name=data.dataset_name,
            version=data.version,
            producer=data.producer,
            consumers=data.consumers,
            schema_spec=[c.dict() for c in data.schema_spec],
            sla_max_freshness_minutes=data.sla_max_freshness_minutes,
            sla_min_quality_score=data.sla_min_quality_score,
            status="ACTIVE"
        )
        db.add(contract)
        await db.commit()
        await db.refresh(contract)
        logger.info(f"Created Data Contract for '{contract.dataset_name}' (id={contract.id})")
        return contract

    @staticmethod
    async def list_contracts(db: AsyncSession, workspace_id: str) -> List[DataContractModel]:
        stmt = select(DataContractModel).where(DataContractModel.workspace_id == workspace_id).order_by(DataContractModel.created_at.desc())
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_contract_by_id(db: AsyncSession, contract_id: str, workspace_id: str) -> DataContractModel:
        stmt = select(DataContractModel).where(
            DataContractModel.id == contract_id,
            DataContractModel.workspace_id == workspace_id
        )
        result = await db.execute(stmt)
        contract = result.scalar_one_or_none()
        if not contract:
            raise NotFoundError("DataContract", contract_id)
        return contract
