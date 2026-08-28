"""
DataFlowX Datasets & Catalog Endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.deps import get_active_workspace_id, get_async_db, get_current_user
from backend.database.models import User
from backend.schemas.common import PaginatedResponse, PaginationParams
from backend.schemas.dataset import DatasetCreate, DatasetOut, ProfilingReportOut
from backend.services.dataset_service import DatasetService

router = APIRouter(prefix="/datasets", tags=["Datasets & Catalog"])


@router.get("", response_model=PaginatedResponse[DatasetOut])
async def list_datasets(
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size, search=search)
    datasets, total = await DatasetService.list_datasets(session, workspace_id, params)
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    return PaginatedResponse(
        items=[
            DatasetOut(
                id=d.id,
                organization_id=d.organization_id,
                workspace_id=d.workspace_id,
                source_id=d.source_id,
                name=d.name,
                slug=d.slug,
                description=d.description,
                layer=d.layer,
                format=d.format,
                storage_path=d.storage_path,
                record_count=d.record_count,
                size_bytes=d.size_bytes,
                quality_score=d.quality_score,
                partition_keys=d.partition_keys or [],
                tags=d.tags or [],
                owner_email=d.owner_email,
                is_active=d.is_active,
                created_at=d.created_at,
                updated_at=d.updated_at,
                versions=[]
            )
            for d in datasets
        ],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=(page < total_pages),
        has_prev=(page > 1)
    )


@router.post("", response_model=DatasetOut, status_code=status.HTTP_201_CREATED)
async def create_dataset(
    payload: DatasetCreate,
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    ds = await DatasetService.create_dataset(session, workspace_id, payload)
    return DatasetOut(
        id=ds.id,
        organization_id=ds.organization_id,
        workspace_id=ds.workspace_id,
        source_id=ds.source_id,
        name=ds.name,
        slug=ds.slug,
        description=ds.description,
        layer=ds.layer,
        format=ds.format,
        storage_path=ds.storage_path,
        record_count=ds.record_count,
        size_bytes=ds.size_bytes,
        quality_score=ds.quality_score,
        partition_keys=ds.partition_keys or [],
        tags=ds.tags or [],
        owner_email=ds.owner_email,
        is_active=ds.is_active,
        created_at=ds.created_at,
        updated_at=ds.updated_at,
        versions=[]
    )


@router.get("/{dataset_id}", response_model=DatasetOut)
async def get_dataset(
    dataset_id: str,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    ds = await DatasetService.get_dataset(session, dataset_id)
    return DatasetOut(
        id=ds.id,
        organization_id=ds.organization_id,
        workspace_id=ds.workspace_id,
        source_id=ds.source_id,
        name=ds.name,
        slug=ds.slug,
        description=ds.description,
        layer=ds.layer,
        format=ds.format,
        storage_path=ds.storage_path,
        record_count=ds.record_count,
        size_bytes=ds.size_bytes,
        quality_score=ds.quality_score,
        partition_keys=ds.partition_keys or [],
        tags=ds.tags or [],
        owner_email=ds.owner_email,
        is_active=ds.is_active,
        created_at=ds.created_at,
        updated_at=ds.updated_at,
        versions=[]
    )


@router.post("/{dataset_id}/profile", response_model=ProfilingReportOut)
async def profile_dataset(
    dataset_id: str,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    report = await DatasetService.profile_dataset(session, dataset_id)
    return ProfilingReportOut(
        id=report.id,
        dataset_id=report.dataset_id,
        dataset_version_id=report.dataset_version_id,
        total_rows=report.total_rows,
        total_columns=report.total_columns,
        null_cells=report.null_cells,
        duplicate_rows=report.duplicate_rows,
        memory_bytes=report.memory_bytes,
        columns_profile=report.columns_profile_json,
        created_at=report.created_at
    )
