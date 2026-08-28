"""
DataFlowX Organizations & Workspaces API Endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.deps import get_async_db, get_current_user
from backend.database.models import User
from backend.schemas.common import PaginatedResponse, PaginationParams
from backend.schemas.organization import (
    OrganizationCreate,
    OrganizationOut,
    OrganizationUpdate,
    WorkspaceCreate,
    WorkspaceOut,
    WorkspaceUpdate,
)
from backend.services.org_service import OrganizationService

router = APIRouter(prefix="/organizations", tags=["Organizations & Multi-tenancy"])


@router.get("", response_model=PaginatedResponse[OrganizationOut])
async def list_organizations(
    page: int = 1,
    page_size: int = 20,
    search: str = None,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size, search=search)
    orgs, total = await OrganizationService.list_organizations(session, params)
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    return PaginatedResponse(
        items=[OrganizationOut.model_validate(o) for o in orgs],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=(page < total_pages),
        has_prev=(page > 1)
    )


@router.post("", response_model=OrganizationOut, status_code=status.HTTP_201_CREATED)
async def create_organization(
    payload: OrganizationCreate,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    org = await OrganizationService.create_organization(session, payload)
    return OrganizationOut.model_validate(org)


@router.get("/{org_id}/workspaces", response_model=List[WorkspaceOut])
async def list_workspaces(
    org_id: str,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    workspaces = await OrganizationService.list_workspaces(session, org_id)
    return [WorkspaceOut.model_validate(w) for w in workspaces]


@router.post("/{org_id}/workspaces", response_model=WorkspaceOut, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    org_id: str,
    payload: WorkspaceCreate,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    ws = await OrganizationService.create_workspace(session, org_id, payload)
    return WorkspaceOut.model_validate(ws)
