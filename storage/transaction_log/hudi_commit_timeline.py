"""
DataFlowX Apache Hudi Timeline Instant & Metadata Parser
Tracks Hudi active and archived timeline actions (commit, deltacommit, compaction, clean, rollback, savepoint).
"""

from typing import List, Optional
from pydantic import BaseModel


class HudiInstant(BaseModel):
    timestamp: str
    action: str  # commit, deltacommit, clean, rollback, compaction
    state: str   # REQUESTED, INFLIGHT, COMPLETED


class HudiTimeline:
    """Parses and queries Hudi timeline instants."""

    def __init__(self, instants: Optional[List[HudiInstant]] = None):
        self.instants = instants or []

    def get_completed_commits(self) -> List[HudiInstant]:
        return [i for i in self.instants if i.state == "COMPLETED" and i.action in ("commit", "deltacommit")]

    def get_latest_commit_timestamp(self) -> Optional[str]:
        commits = self.get_completed_commits()
        if commits:
            return sorted(commits, key=lambda x: x.timestamp)[-1].timestamp
        return None
