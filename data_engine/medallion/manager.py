"""
DataFlowX Medallion Data Lake Manager
Governs data movement across Bronze (Raw Immutable), Silver (Cleaned/Validated), and Gold (Aggregated Business Marts).
"""

from datetime import datetime, timezone
import os
from typing import Any, Dict, List, Optional
import pandas as pd
from backend.core.logging import get_logger
from storage import ParquetManager, storage_engine

logger = get_logger(__name__)


class MedallionManager:
    """Enterprise Medallion Architecture Manager."""

    @staticmethod
    def store_bronze(
        records: List[Dict[str, Any]],
        dataset_name: str,
        execution_id: str,
        partition_date: Optional[str] = None
    ) -> str:
        """Persist raw immutable ingested batch into Bronze layer."""
        date_key = partition_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        storage_key = f"bronze/{dataset_name}/{date_key}/{execution_id[:8]}.parquet"
        parquet_bytes = ParquetManager.records_to_parquet_bytes(records)
        storage_engine.put_object(storage_key, parquet_bytes)
        logger.info(f"Stored {len(records)} records in Bronze layer: {storage_key}")
        return storage_key

    @staticmethod
    def store_silver(
        records: List[Dict[str, Any]],
        dataset_name: str,
        execution_id: str,
        version: int = 1
    ) -> str:
        """Persist cleaned, validated, and deduplicated records into Silver layer."""
        storage_key = f"silver/{dataset_name}/v{version}/{execution_id[:8]}.parquet"
        parquet_bytes = ParquetManager.records_to_parquet_bytes(records)
        storage_engine.put_object(storage_key, parquet_bytes)
        logger.info(f"Stored {len(records)} records in Silver layer: {storage_key}")
        return storage_key

    @staticmethod
    def store_gold(
        records: List[Dict[str, Any]],
        dataset_name: str,
        execution_id: str,
        version: int = 1
    ) -> str:
        """Persist aggregated, business-ready analytical records into Gold layer."""
        storage_key = f"gold/{dataset_name}/v{version}/{execution_id[:8]}.parquet"
        parquet_bytes = ParquetManager.records_to_parquet_bytes(records)
        storage_engine.put_object(storage_key, parquet_bytes)
        logger.info(f"Stored {len(records)} records in Gold layer: {storage_key}")
        return storage_key

    @staticmethod
    def load_layer_dataset(layer: str, dataset_name: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Read and union all Parquet files for a dataset in a specific medallion layer."""
        prefix = f"{layer}/{dataset_name}/"
        objects = storage_engine.list_objects(prefix)
        all_records: List[Dict[str, Any]] = []

        for obj_key in objects:
            if obj_key.endswith(".parquet"):
                try:
                    data = storage_engine.get_object(obj_key)
                    recs = ParquetManager.parquet_bytes_to_records(data)
                    all_records.extend(recs)
                    if limit and len(all_records) >= limit:
                        return all_records[:limit]
                except Exception as exc:
                    logger.warning(f"Could not read parquet object {obj_key}: {exc}")

        return all_records
