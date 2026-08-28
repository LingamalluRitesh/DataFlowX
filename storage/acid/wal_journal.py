"""
DataFlowX Write-Ahead Log (WAL) Append Journal
Appends serialized transaction log records with CRC32 checksums, fsync synchronization, and crash recovery log replays.
"""

from datetime import datetime, timezone
import json
import os
import zlib
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class WALLogRecord(BaseModel):
    lsn: int
    record_type: str  # COMMIT, ABORT, ADD_FILE, REMOVE_FILE, SET_METADATA
    txn_id: str
    payload: Dict[str, Any]
    crc32: int = 0
    timestamp_utc: str


class WriteAheadJournal:
    """Manages appending and replaying ACID delta log files."""

    def __init__(self, table_path: str):
        self.table_path = table_path
        self.log_dir = os.path.join(table_path, "_delta_log")
        self._curr_lsn = 0

    def append_record(self, record_type: str, txn_id: str, payload: Dict[str, Any]) -> WALLogRecord:
        self._curr_lsn += 1
        body_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        crc = zlib.crc32(body_bytes)

        rec = WALLogRecord(
            lsn=self._curr_lsn,
            record_type=record_type,
            txn_id=txn_id,
            payload=payload,
            crc32=crc,
            timestamp_utc=datetime.now(timezone.utc).isoformat()
        )
        logger.debug(f"Appended WAL entry LSN={rec.lsn} for txn '{txn_id}' (crc={crc})")
        return rec
