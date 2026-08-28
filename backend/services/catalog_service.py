"""
DataFlowX Data Catalog & Business Glossary Service
"""

from typing import Any, Dict, List, Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exceptions import NotFoundError
from backend.core.logging import get_logger
from backend.database.models.governance import CatalogAssetModel, GlossaryTermModel
from backend.schemas.governance import CatalogAssetCreate, GlossaryTermCreate

logger = get_logger(__name__)


class CatalogService:
    """Business service for enterprise metadata catalog and glossary operations."""

    @staticmethod
    async def create_asset(db: AsyncSession, workspace_id: str, data: CatalogAssetCreate) -> CatalogAssetModel:
        asset = CatalogAssetModel(
            workspace_id=workspace_id,
            name=data.name,
            layer=data.layer,
            domain=data.domain,
            owner=data.owner,
            description=data.description,
            storage_uri=data.storage_uri,
            columns_metadata=[c.dict() for c in data.columns_metadata],
            tags=data.tags
        )
        db.add(asset)
        await db.commit()
        await db.refresh(asset)
        logger.info(f"Created catalog asset '{asset.name}' (id={asset.id})")
        return asset

    @staticmethod
    async def list_assets(
        db: AsyncSession,
        workspace_id: str,
        domain: Optional[str] = None,
        layer: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[CatalogAssetModel]:
        stmt = select(CatalogAssetModel).where(CatalogAssetModel.workspace_id == workspace_id)
        if domain:
            stmt = stmt.where(CatalogAssetModel.domain == domain)
        if layer:
            stmt = stmt.where(CatalogAssetModel.layer == layer)
        if search:
            stmt = stmt.where(CatalogAssetModel.name.ilike(f"%{search}%"))

        stmt = stmt.order_by(CatalogAssetModel.name.asc())
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_asset_by_id(db: AsyncSession, asset_id: str, workspace_id: str) -> CatalogAssetModel:
        stmt = select(CatalogAssetModel).where(
            CatalogAssetModel.id == asset_id,
            CatalogAssetModel.workspace_id == workspace_id
        )
        result = await db.execute(stmt)
        asset = result.scalar_one_or_none()
        if not asset:
            raise NotFoundError("CatalogAsset", asset_id)
        return asset

    @staticmethod
    async def create_glossary_term(db: AsyncSession, workspace_id: str, data: GlossaryTermCreate) -> GlossaryTermModel:
        term = GlossaryTermModel(
            workspace_id=workspace_id,
            term=data.term,
            definition=data.definition,
            domain=data.domain,
            owner_email=data.owner_email,
            synonyms=data.synonyms,
            tags=data.tags
        )
        db.add(term)
        await db.commit()
        await db.refresh(term)
        return term

    @staticmethod
    async def list_glossary_terms(db: AsyncSession, workspace_id: str, domain: Optional[str] = None) -> List[GlossaryTermModel]:
        stmt = select(GlossaryTermModel).where(GlossaryTermModel.workspace_id == workspace_id)
        if domain:
            stmt = stmt.where(GlossaryTermModel.domain == domain)
        stmt = stmt.order_by(GlossaryTermModel.term.asc())
        result = await db.execute(stmt)
        return list(result.scalars().all())
