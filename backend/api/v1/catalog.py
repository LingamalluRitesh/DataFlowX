"""
Data Catalog and Business Glossary REST API Endpoints
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.v1.deps import get_current_user
from backend.core.database import get_async_db
from backend.database.models.user import User
from backend.schemas.governance import (
    CatalogAssetCreate,
    CatalogAssetOut,
    GlossaryTermCreate,
    GlossaryTermOut,
)
from backend.services.catalog_service import CatalogService

router = APIRouter(prefix="/catalog", tags=["Data Catalog & Glossary"])


@router.get("/assets", response_model=List[CatalogAssetOut])
async def list_catalog_assets(
    domain: Optional[str] = Query(None),
    layer: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """List all indexed data assets in workspace catalog."""
    workspace_id = current_user.workspaces[0].workspace_id if current_user.workspaces else "ws_default"
    return await CatalogService.list_assets(db, workspace_id, domain=domain, layer=layer, search=search)


@router.post("/assets", response_model=CatalogAssetOut, status_code=status.HTTP_201_CREATED)
async def create_catalog_asset(
    payload: CatalogAssetCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Register a new dataset asset in the catalog."""
    workspace_id = current_user.workspaces[0].workspace_id if current_user.workspaces else "ws_default"
    return await CatalogService.create_asset(db, workspace_id, payload)


@router.get("/assets/{asset_id}", response_model=CatalogAssetOut)
async def get_catalog_asset(
    asset_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Fetch single catalog asset details."""
    workspace_id = current_user.workspaces[0].workspace_id if current_user.workspaces else "ws_default"
    return await CatalogService.get_asset_by_id(db, asset_id, workspace_id)


@router.get("/glossary", response_model=List[GlossaryTermOut])
async def list_glossary_terms(
    domain: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """List business glossary terms."""
    workspace_id = current_user.workspaces[0].workspace_id if current_user.workspaces else "ws_default"
    return await CatalogService.list_glossary_terms(db, workspace_id, domain=domain)


@router.post("/glossary", response_model=GlossaryTermOut, status_code=status.HTTP_201_CREATED)
async def create_glossary_term(
    payload: GlossaryTermCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Add term to business glossary."""
    workspace_id = current_user.workspaces[0].workspace_id if current_user.workspaces else "ws_default"
    return await CatalogService.create_glossary_term(db, workspace_id, payload)
