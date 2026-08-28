"""
DataFlowX Write-Ahead Log (WAL) Transaction Boundary Coordinator
Buffers out-of-order CDC change events within active transaction IDs (XIDs) and releases atomic committed micro-batches.
"""

from collections import defaultdict
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CDCOperation(BaseModel):
    xid: int
    lsn: int
    table: str
    op_type: str  # c (CREATE/INSERT), u (UPDATE), d (DELETE), r (READ/SNAPSHOT)
    before: Optional[Dict[str, Any]] = None
    after: Optional[Dict[str, Any]] = None
    timestamp_ms: int


class WALTransactionBuffer:
    """Buffers in-flight transactions until explicit COMMIT."""

    def __init__(self):
        # xid -> list of CDCOperation
        self._inflight: Dict[int, List[CDCOperation]] = defaultdict(list)
        self.committed_batches: List[List[CDCOperation]] = []

    def record_operation(self, op: CDCOperation) -> None:
        self._inflight[op.xid].append(op)

    def commit_transaction(self, xid: int) -> Optional[List[CDCOperation]]:
        if xid in self._inflight:
            ops = self._inflight.pop(xid)
            self.committed_batches.append(ops)
            return ops
        return None

    def rollback_transaction(self, xid: int) -> None:
        self._inflight.pop(xid, None)
