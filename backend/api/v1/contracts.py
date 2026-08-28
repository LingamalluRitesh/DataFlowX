"""
Data Contracts REST API Endpoints
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.v1.deps import get_current_user
from backend.core.database import get_async_db
from backend.database.models.user import User
from backend.schemas.governance import DataContractCreate, DataContractOut
from backend.services.contract_service import ContractService

router = APIRouter(prefix="/contracts", tags=["Data Contracts & SLAs"])


@router.get("", response_model=List[DataContractOut])
async def list_data_contracts(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """List all active data contracts in current workspace."""
    workspace_id = current_user.workspaces[0].workspace_id if current_user.workspaces else "ws_default"
    return await ContractService.list_contracts(db, workspace_id)


@router.post("", response_model=DataContractOut, status_code=status.HTTP_201_CREATED)
async def create_data_contract(
    payload: DataContractCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Create a new producer-consumer data contract specification."""
    workspace_id = current_user.workspaces[0].workspace_id if current_user.workspaces else "ws_default"
    return await ContractService.create_contract(db, workspace_id, payload)


@router.get("/{contract_id}", response_model=DataContractOut)
async def get_data_contract(
    contract_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve specific data contract details."""
    workspace_id = current_user.workspaces[0].workspace_id if current_user.workspaces else "ws_default"
    return await ContractService.get_contract_by_id(db, contract_id, workspace_id)
