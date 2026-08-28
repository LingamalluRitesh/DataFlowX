"""
DataFlowX Parquet Small-File Compaction & Bin-Packing Optimizer
Solves the lakehouse small-file problem by merging sub-optimal micro-files into target 128MB-512MB compressed row groups.
"""

from datetime import datetime, timezone
import os
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class CompactionCandidate(BaseModel):
    file_path: str
    size_bytes: int
    record_count: int


class CompactionPlan(BaseModel):
    plan_id: str
    target_bin_size_bytes: int = 134217728  # 128 MB
    bins: List[List[CompactionCandidate]] = Field(default_factory=list)
    total_files_before: int = 0
    estimated_files_after: int = 0


class ParquetCompactor:
    """Implements First-Fit Decreasing (FFD) bin-packing for lakehouse compaction."""

    @staticmethod
    def plan_compaction(
        candidates: List[CompactionCandidate],
        target_bin_size_bytes: int = 134217728
    ) -> CompactionPlan:
        # Sort candidates descending by file size
        sorted_files = sorted(candidates, key=lambda c: c.size_bytes, reverse=True)
        bins: List[List[CompactionCandidate]] = []
        bin_sizes: List[int] = []

        for f in sorted_files:
            placed = False
            for b_idx, current_size in enumerate(bin_sizes):
                if current_size + f.size_bytes <= target_bin_size_bytes:
                    bins[b_idx].append(f)
                    bin_sizes[b_idx] += f.size_bytes
                    placed = True
                    break

            if not placed:
                bins.append([f])
                bin_sizes.append(f.size_bytes)

        plan = CompactionPlan(
            plan_id=f"plan_compact_{int(datetime.now(timezone.utc).timestamp())}",
            target_bin_size_bytes=target_bin_size_bytes,
            bins=bins,
            total_files_before=len(candidates),
            estimated_files_after=len(bins)
        )
        logger.info(f"Generated compaction plan: {len(candidates)} files -> {len(bins)} target bins")
        return plan
