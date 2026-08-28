"""
DataFlowX Data Sources & Connectors Endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.deps import get_active_workspace_id, get_async_db, get_current_user
from backend.database.models import User
from backend.schemas.common import PaginatedResponse, PaginationParams, StatusMessage
from backend.schemas.source import (
    ConnectionTestRequest,
    ConnectionTestResponse,
    DataSourceCreate,
    DataSourceOut,
    DataSourceUpdate,
    SchemaDiscoveryResponse,
)
from backend.services.source_service import SourceService
from connectors.registry import ConnectorRegistry

router = APIRouter(prefix="/sources", tags=["Data Sources"])


@router.get("/connectors", response_model=List[str])
async def list_available_connectors(_: User = Depends(get_current_user)):
    """List all registered connector types."""
    return ConnectorRegistry.list_available_connectors()


@router.get("", response_model=PaginatedResponse[DataSourceOut])
async def list_sources(
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size, search=search)
    sources, total = await SourceService.list_sources(session, workspace_id, params)
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    return PaginatedResponse(
        items=[
            DataSourceOut(
                id=s.id,
                organization_id=s.organization_id,
                workspace_id=s.workspace_id,
                name=s.name,
                slug=s.slug,
                connector_type=s.connector_type,
                description=s.description,
                status=s.status,
                health_status=s.health_status,
                config=s.config or {},
                is_active=s.is_active,
                last_synced_at=s.last_synced_at,
                last_health_check_at=s.last_health_check_at,
                created_at=s.created_at,
                updated_at=s.updated_at,
                has_credentials=bool(s.credentials)
            )
            for s in sources
        ],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=(page < total_pages),
        has_prev=(page > 1)
    )


@router.post("", response_model=DataSourceOut, status_code=status.HTTP_201_CREATED)
async def create_source(
    payload: DataSourceCreate,
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    source = await SourceService.create_source(session, workspace_id, payload)
    return DataSourceOut(
        id=source.id,
        organization_id=source.organization_id,
        workspace_id=source.workspace_id,
        name=source.name,
        slug=source.slug,
        connector_type=source.connector_type,
        description=source.description,
        status=source.status,
        health_status=source.health_status,
        config=source.config or {},
        is_active=source.is_active,
        created_at=source.created_at,
        updated_at=source.updated_at,
        has_credentials=bool(payload.credentials)
    )


@router.get("/{source_id}", response_model=DataSourceOut)
async def get_source(
    source_id: str,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    source = await SourceService.get_source(session, source_id)
    return DataSourceOut(
        id=source.id,
        organization_id=source.organization_id,
        workspace_id=source.workspace_id,
        name=source.name,
        slug=source.slug,
        connector_type=source.connector_type,
        description=source.description,
        status=source.status,
        health_status=source.health_status,
        config=source.config or {},
        is_active=source.is_active,
        created_at=source.created_at,
        updated_at=source.updated_at,
        has_credentials=bool(source.credentials)
    )


@router.post("/{source_id}/test", response_model=ConnectionTestResponse)
async def test_source_connection(
    source_id: str,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    return await SourceService.test_connection(session, source_id)


@router.post("/{source_id}/discover-schema", response_model=SchemaDiscoveryResponse)
async def discover_source_schema(
    source_id: str,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    return await SourceService.discover_schema(session, source_id)


@router.delete("/{source_id}", response_model=StatusMessage)
async def delete_source(
    source_id: str,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    await SourceService.delete_source(session, source_id)
    return StatusMessage(success=True, message=f"Data source '{source_id}' deleted successfully")
