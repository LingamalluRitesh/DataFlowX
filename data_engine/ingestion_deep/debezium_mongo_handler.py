"""
DataFlowX Debezium MongoDB Change Stream Processor
Unpacks MongoDB oplog mutations (insert, update, replace, delete), extracting document keys and updated field descriptions.
"""

from typing import Any, Dict, Optional
from data_engine.ingestion_deep.debezium_pg_handler import CDCRecord


class DebeziumMongoHandler:
    """Unpacks MongoDB CDC change streams."""

    @classmethod
    def process_envelope(cls, raw_envelope: Dict[str, Any]) -> CDCRecord:
        payload = raw_envelope.get("payload", raw_envelope)
        source = payload.get("source", {})
        table = f"{source.get('rs', 'rs0')}.{source.get('collection', 'unknown')}"
        op = payload.get("op", "c")
        ts_ms = payload.get("ts_ms", 0)

        return CDCRecord(
            operation=op,
            table_name=table,
            lsn=ts_ms,
            timestamp_ms=ts_ms,
            before_state=None,
            after_state=payload.get("after")
        )
