"""
DataFlowX Enterprise Data Catalog & Metadata Management
Provides data asset indexing, business glossary terms, automated tagging, domain classification, and dataset ownership.
"""

from datetime import datetime, timezone
import json
from typing import Any, Dict, List, Optional, Set, Union
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class GlossaryTerm(BaseModel):
    id: str
    term: str
    definition: str
    domain: str  # e.g., Finance, Marketing, Operations, Engineering
    owner_email: str
    synonyms: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CatalogColumnMetadata(BaseModel):
    name: str
    data_type: str
    description: Optional[str] = None
    is_primary_key: bool = False
    is_foreign_key: bool = False
    is_pii: bool = False
    pii_category: Optional[str] = None  # EMAIL, PHONE, SSN, FINANCIAL, ADDRESS
    glossary_terms: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class CatalogAsset(BaseModel):
    id: str
    name: str
    layer: str  # BRONZE, SILVER, GOLD, WAREHOUSE, EXTERNAL_SOURCE
    storage_uri: Optional[str] = None
    description: Optional[str] = None
    domain: str = "Enterprise"
    owner: str = "data-team@dataflowx.io"
    columns: List[CatalogColumnMetadata] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    last_profiled_at: Optional[str] = None
    quality_score: Optional[float] = 100.0
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EnterpriseDataCatalog:
    """In-memory and persistent Data Catalog index for data discovery."""

    def __init__(self):
        self._assets: Dict[str, CatalogAsset] = {}
        self._glossary: Dict[str, GlossaryTerm] = {}

    def register_asset(self, asset: CatalogAsset) -> CatalogAsset:
        self._assets[asset.id] = asset
        logger.info(f"Registered Catalog Asset '{asset.name}' (id={asset.id}, domain={asset.domain})")
        return asset

    def search_assets(self, query: str, domain: Optional[str] = None, tag: Optional[str] = None) -> List[CatalogAsset]:
        q = query.lower()
        results = []
        for a in self._assets.values():
            if domain and a.domain.lower() != domain.lower():
                continue
            if tag and tag.lower() not in [t.lower() for t in a.tags]:
                continue
            if q in a.name.lower() or (a.description and q in a.description.lower()):
                results.append(a)
        return results

    def add_glossary_term(self, term: GlossaryTerm) -> GlossaryTerm:
        self._glossary[term.id] = term
        return term

    def list_glossary_terms(self, domain: Optional[str] = None) -> List[GlossaryTerm]:
        if domain:
            return [t for t in self._glossary.values() if t.domain.lower() == domain.lower()]
        return list(self._glossary.values())
