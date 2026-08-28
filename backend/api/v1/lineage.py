"""
DataFlowX Data Lineage & Governance API Endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.deps import get_active_workspace_id, get_async_db, get_current_user
from backend.database.models import User
from backend.schemas.lineage import (
    DataContractCreate,
    DataContractOut,
    LineageGraphOut,
    TagCreate,
    TagOut,
)
from backend.services.lineage_service import LineageService

router = APIRouter(prefix="/lineage", tags=["Data Lineage & Governance"])


@router.get("/graph", response_model=LineageGraphOut)
async def get_lineage_graph(
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    """Retrieve end-to-end data provenance graph for the active workspace."""
    return await LineageService.get_lineage_graph(session, workspace_id)


@router.post("/contracts", response_model=DataContractOut, status_code=status.HTTP_201_CREATED)
async def create_data_contract(
    payload: DataContractCreate,
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    contract = await LineageService.create_data_contract(session, workspace_id, payload)
    return DataContractOut(
        id=contract.id,
        organization_id=contract.organization_id,
        workspace_id=contract.workspace_id,
        name=contract.name,
        dataset_id=contract.dataset_id,
        schema_version_id=contract.schema_version_id,
        sla_freshness_hours=contract.sla_freshness_hours,
        min_quality_score=contract.min_quality_score,
        max_null_percentage=contract.max_null_percentage,
        owner_email=contract.owner_email,
        status=contract.status,
        created_at=contract.created_at,
        updated_at=contract.updated_at
    )


@router.post("/tags", response_model=TagOut, status_code=status.HTTP_201_CREATED)
async def create_tag(
    payload: TagCreate,
    session: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    tag = await LineageService.create_tag(session, "default_org", payload)
    return TagOut(
        id=tag.id,
        organization_id=tag.organization_id,
        name=tag.name,
        color=tag.color,
        category=tag.category,
        description=tag.description,
        created_at=tag.created_at
    )
