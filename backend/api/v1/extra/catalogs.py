from typing import Any, Dict, List
from fastapi import APIRouter
from storage.catalogs.rest_catalog import IcebergRESTCatalogClient

router = APIRouter(prefix="/catalogs", tags=["Lakehouse Catalogs"])
_iceberg = IcebergRESTCatalogClient()


@router.get("/namespaces")
def list_catalog_namespaces() -> List[List[str]]:
    return _iceberg.list_namespaces()


@router.get("/tables")
def list_catalog_tables(namespace: str = "gold") -> List[Dict[str, Any]]:
    tables = _iceberg.list_tables(namespace)
    return [t.dict() for t in tables]
