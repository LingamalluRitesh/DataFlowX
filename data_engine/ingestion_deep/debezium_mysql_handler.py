"""
DataFlowX Debezium MySQL Binlog CDC Processor
Unpacks MySQL row-event binary log change streams, extracting binlog file names, positions, and server IDs.
"""

from typing import Any, Dict, Optional
from data_engine.ingestion_deep.debezium_pg_handler import CDCRecord


class DebeziumMySQLHandler:
    """Unpacks MySQL CDC events."""

    @classmethod
    def process_envelope(cls, raw_envelope: Dict[str, Any]) -> CDCRecord:
        payload = raw_envelope.get("payload", raw_envelope)
        source = payload.get("source", {})
        table = f"{source.get('db', 'default')}.{source.get('table', 'unknown')}"
        op = payload.get("op", "c")
        pos = source.get("pos", 0)
        ts_ms = payload.get("ts_ms", 0)

        return CDCRecord(
            operation=op,
            table_name=table,
            lsn=pos,
            timestamp_ms=ts_ms,
            before_state=payload.get("before"),
            after_state=payload.get("after")
        )
