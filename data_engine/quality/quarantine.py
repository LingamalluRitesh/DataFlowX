"""
DataFlowX Quarantine Manager
Captures and persists invalid or rejected records for auditing and remediation.
"""

from datetime import datetime, timezone
import json
import os
from typing import Any, Dict, List, Optional
import pandas as pd
from backend.core.logging import get_logger
from storage import ParquetManager, storage_engine

logger = get_logger(__name__)


class QuarantineManager:
    """Manages quarantined records and metadata."""

    def __init__(self, base_storage_key: str = "quarantine"):
        self.base_storage_key = base_storage_key

    def quarantine_records(
        self,
        records: List[Dict[str, Any]],
        dataset_id: str,
        execution_id: str,
        rule_name: str,
        reason: str,
    ) -> str:
        """Store quarantined records into partitioned Parquet storage."""
        if not records:
            return ""

        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m-%d")
        storage_key = f"{self.base_storage_key}/{dataset_id}/{date_str}/{execution_id[:8]}_{rule_name}.parquet"

        quarantined_payloads = []
        for r in records:
            quarantined_payloads.append({
                "_dfx_dataset_id": dataset_id,
                "_dfx_execution_id": execution_id,
                "_dfx_rule_name": rule_name,
                "_dfx_quarantine_reason": reason,
                "_dfx_quarantined_at": now.isoformat(),
                "payload": json.dumps(r, default=str),
            })

        parquet_bytes = ParquetManager.records_to_parquet_bytes(quarantined_payloads)
        storage_engine.put_object(storage_key, parquet_bytes, content_type="application/octet-stream")
        logger.info(f"Quarantined {len(records)} records to {storage_key} due to rule '{rule_name}' failure")
        return storage_key
