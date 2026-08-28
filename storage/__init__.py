"""
DataFlowX Storage Layer Exporter
"""

from backend.core.config import settings
from storage.base import BaseObjectStore
from storage.local_store import LocalFileStore
from storage.parquet_manager import ParquetManager
from storage.s3_store import S3ObjectStore


def get_storage_engine() -> BaseObjectStore:
    """Instantiate storage provider according to platform settings."""
    if settings.STORAGE_TYPE in ("s3", "minio"):
        return S3ObjectStore()
    return LocalFileStore(base_path=settings.LOCAL_STORAGE_BASE_PATH)


# Storage singleton
storage_engine = get_storage_engine()

__all__ = [
    "BaseObjectStore",
    "LocalFileStore",
    "S3ObjectStore",
    "ParquetManager",
    "get_storage_engine",
    "storage_engine",
]
