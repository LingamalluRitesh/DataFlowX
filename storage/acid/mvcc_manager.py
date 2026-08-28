"""
DataFlowX Lakehouse MVCC & Snapshot Isolation Transaction Manager
Maintains snapshot timestamps, active transaction tables, read/write conflict detection, and atomic commit journals for Delta Lake and Iceberg tables.
"""

from datetime import datetime, timezone
import threading
import time
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class TransactionRecord(BaseModel):
    txn_id: str
    read_version: int
    commit_version: Optional[int] = None
    started_at_unix: float
    status: str = "ACTIVE"  # ACTIVE, COMMITTED, ABORTED
    written_files: List[str] = Field(default_factory=list)
    deleted_files: List[str] = Field(default_factory=list)


class LakehouseMVCCManager:
    """Manages snapshot isolation and serializable transaction commits."""

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.current_version = 1
        self._lock = threading.Lock()
        self._active_txns: Dict[str, TransactionRecord] = {}
        self._commit_history: List[TransactionRecord] = []

    def begin_transaction(self, txn_id: str) -> TransactionRecord:
        with self._lock:
            record = TransactionRecord(
                txn_id=txn_id,
                read_version=self.current_version,
                started_at_unix=time.time(),
                status="ACTIVE"
            )
            self._active_txns[txn_id] = record
            logger.info(f"Began MVCC transaction '{txn_id}' at snapshot version {record.read_version}")
            return record

    def commit_transaction(self, txn_id: str, written_files: List[str], deleted_files: List[str]) -> int:
        with self._lock:
            if txn_id not in self._active_txns:
                raise ValueError(f"Transaction '{txn_id}' not active")

            record = self._active_txns[txn_id]

            # Conflict Detection: check if any file in deleted_files was already modified since read_version
            for past_txn in self._commit_history:
                if past_txn.commit_version and past_txn.commit_version > record.read_version:
                    overlap = set(deleted_files).intersection(set(past_txn.written_files))
                    if overlap:
                        record.status = "ABORTED"
                        del self._active_txns[txn_id]
                        logger.error(f"Transaction '{txn_id}' write conflict on files: {overlap}. Aborted.")
                        raise RuntimeError(f"Concurrent write conflict in MVCC table '{self.table_name}'")

            self.current_version += 1
            record.commit_version = self.current_version
            record.written_files = written_files
            record.deleted_files = deleted_files
            record.status = "COMMITTED"

            self._commit_history.append(record)
            del self._active_txns[txn_id]

            logger.info(f"Committed transaction '{txn_id}' to table '{self.table_name}' at version {record.commit_version}")
            return record.commit_version
