"""
DataFlowX Delta Lake JSON Commit Log & Checkpoint Replayer
Replays Delta Lake JSON commits (`000000.json`) and compacts AddFile / RemoveFile actions to determine current active data files.
"""

import json
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field


class DeltaAddFileAction(BaseModel):
    path: str
    size_bytes: int
    modification_time: int
    data_change: bool = True
    partition_values: Dict[str, str] = Field(default_factory=dict)
    stats: Optional[str] = None


class DeltaRemoveFileAction(BaseModel):
    path: str
    deletion_timestamp: int
    data_change: bool = True


class DeltaCommitReplayer:
    """Replays Delta commits to construct active table state."""

    def __init__(self):
        self.active_files: Dict[str, DeltaAddFileAction] = {}
        self.version = 0

    def replay_commit_json(self, commit_lines: List[str]) -> None:
        self.version += 1
        for line in commit_lines:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if "add" in entry:
                    add_obj = DeltaAddFileAction(
                        path=entry["add"]["path"],
                        size_bytes=entry["add"].get("size", 0),
                        modification_time=entry["add"].get("modificationTime", 0),
                        partition_values=entry["add"].get("partitionValues", {}),
                        stats=entry["add"].get("stats")
                    )
                    self.active_files[add_obj.path] = add_obj
                elif "remove" in entry:
                    rem_path = entry["remove"]["path"]
                    self.active_files.pop(rem_path, None)
            except Exception:
                continue

    def get_active_file_paths(self) -> List[str]:
        return list(self.active_files.keys())

    def get_total_table_size_bytes(self) -> int:
        return sum(f.size_bytes for f in self.active_files.values())
