"""
DataFlowX Debezium PostgreSQL WAL Event Processor
Unpacks PostgreSQL wal2json and pgoutput CDC mutation envelopes, extracting 'before' and 'after' column tuples and transaction LSN markers.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CDCRecord(BaseModel):
    operation: str  # c (create), u (update), d (delete), r (read)
    table_name: str
    lsn: int
    timestamp_ms: int
    before_state: Optional[Dict[str, Any]] = None
    after_state: Optional[Dict[str, Any]] = None


class DebeziumPostgresHandler:
    """Unpacks PostgreSQL CDC events."""

    @classmethod
    def process_envelope(cls, raw_envelope: Dict[str, Any]) -> CDCRecord:
        payload = raw_envelope.get("payload", raw_envelope)
        source = payload.get("source", {})
        table = f"{source.get('schema', 'public')}.{source.get('table', 'unknown')}"
        op = payload.get("op", "c")
        lsn = source.get("lsn", 0)
        ts_ms = payload.get("ts_ms", 0)

        return CDCRecord(
            operation=op,
            table_name=table,
            lsn=lsn,
            timestamp_ms=ts_ms,
            before_state=payload.get("before"),
            after_state=payload.get("after")
        )
