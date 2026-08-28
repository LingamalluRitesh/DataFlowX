"""
DataFlowX Local File System Sensor
Pokes local or NFS mounted file system until a file matches the target path or glob pattern.
"""

import glob
import os
import time
from typing import Any, Dict, Optional

from orchestration_engine.sensors.base_sensor import BaseSensor, SensorResult


class FileSensor(BaseSensor):
    """Monitors local filesystem or network share for arrival of files."""

    def __init__(
        self,
        file_path_or_glob: str,
        min_size_bytes: int = 1,
        name: Optional[str] = None,
        timeout_seconds: int = 3600,
        poke_interval_seconds: int = 30
    ):
        super().__init__(name=name or f"file_sensor_{os.path.basename(file_path_or_glob)}", timeout_seconds=timeout_seconds, poke_interval_seconds=poke_interval_seconds)
        self.file_path_or_glob = file_path_or_glob
        self.min_size_bytes = min_size_bytes

    def poke(self) -> SensorResult:
        matches = glob.glob(self.file_path_or_glob)
        valid_files = []
        for m in matches:
            if os.path.isfile(m) and os.path.getsize(m) >= self.min_size_bytes:
                valid_files.append(m)

        if valid_files:
            return SensorResult(
                is_ready=True,
                message=f"Found {len(valid_files)} matching file(s): {valid_files[:3]}",
                metadata={"matched_files": valid_files, "count": len(valid_files)},
                poked_at=time.time()
            )

        return SensorResult(
            is_ready=False,
            message=f"No matching file found for pattern '{self.file_path_or_glob}'",
            poked_at=time.time()
        )
