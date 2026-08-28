"""
DataFlowX Change Data Capture (CDC) Debezium Event Decoder
Decodes Debezium JSON/Avro envelope structures into relational mutations: INSERT (c), UPDATE (u), DELETE (d), and SNAPSHOT (r).
"""

from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class CDCMutation(BaseModel):
    operation: str  # INSERT, UPDATE, DELETE, READ_SNAPSHOT
    table_name: str
    schema_name: str
    source_timestamp_ms: int
    before_state: Optional[Dict[str, Any]] = None
    after_state: Optional[Dict[str, Any]] = None
    primary_key_values: Dict[str, Any] = Field(default_factory=dict)
    changed_columns: List[str] = Field(default_factory=list)


class DebeziumDecoder:
    """Decodes standard Debezium PostgreSQL/MySQL WAL JSON change envelopes."""

    OP_MAP = {
        "c": "INSERT",
        "u": "UPDATE",
        "d": "DELETE",
        "r": "READ_SNAPSHOT",
    }

    @classmethod
    def decode_envelope(cls, payload: Dict[str, Any]) -> Optional[CDCMutation]:
        op_code = payload.get("op")
        if not op_code or op_code not in cls.OP_MAP:
            return None

        op_name = cls.OP_MAP[op_code]
        source_meta = payload.get("source", {})
        tbl = source_meta.get("table", "unknown_table")
        sch = source_meta.get("schema", "public")
        ts_ms = source_meta.get("ts_ms", 0)

        before = payload.get("before")
        after = payload.get("after")

        changed_cols = []
        if before and after:
            for k, v in after.items():
                if k in before and before[k] != v:
                    changed_cols.append(k)

        return CDCMutation(
            operation=op_name,
            table_name=tbl,
            schema_name=sch,
            source_timestamp_ms=ts_ms,
            before_state=before,
            after_state=after,
            changed_columns=changed_cols
        )
