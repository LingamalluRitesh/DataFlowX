"""
DataFlowX Apache Hudi Timeline Instant Generator
Generates Apache Hudi `.commit`, `.clean`, `.compaction`, and `.rollback` instant timeline metadata markers.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class HudiInstantAction(BaseModel):
    instant_timestamp: str
    action_type: str  # COMMIT, CLEAN, COMPACTION, ROLLBACK
    state: str = "COMPLETED"
    partition_writes: Dict[str, int] = Field(default_factory=dict)


class HudiTimelineGenerator:
    """Generates Hudi timeline commit metadata."""

    @classmethod
    def create_commit_instant(cls, partition_writes: Dict[str, int]) -> HudiInstantAction:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        return HudiInstantAction(
            instant_timestamp=ts,
            action_type="COMMIT",
            state="COMPLETED",
            partition_writes=partition_writes
        )
