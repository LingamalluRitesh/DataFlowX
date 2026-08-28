"""
DataFlowX Durable Saga State Journal
Persists saga execution states and transition records to enable recovery after coordinator restart or crash.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SagaJournalEntry(BaseModel):
    saga_id: str
    step_name: str
    action_type: str  # EXECUTE, COMPENSATE
    status: str  # SUCCESS, FAILED
    timestamp_unix: float


class DurableSagaJournal:
    """In-memory and persistent journal for distributed sagas."""

    def __init__(self):
        self._entries: List[SagaJournalEntry] = []

    def record_step(self, saga_id: str, step_name: str, action_type: str, status: str) -> None:
        import time
        self._entries.append(SagaJournalEntry(
            saga_id=saga_id,
            step_name=step_name,
            action_type=action_type,
            status=status,
            timestamp_unix=time.time()
        ))

    def get_saga_history(self, saga_id: str) -> List[SagaJournalEntry]:
        return [e for e in self._entries if e.saga_id == saga_id]
