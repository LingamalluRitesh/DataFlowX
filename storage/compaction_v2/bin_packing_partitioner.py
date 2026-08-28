"""
DataFlowX First-Fit-Decreasing (FFD) Parquet Bin Packing Partitioner
Groups small files into target file sizes (e.g., 128MB or 512MB) to solve the small-file problem in object stores.
"""

from typing import List, Tuple
from pydantic import BaseModel, Field


class CompactionBin(BaseModel):
    bin_id: int
    file_paths: List[str] = Field(default_factory=list)
    total_size_bytes: int = 0


class BinPackingPartitioner:
    """Partitions files into optimal compaction bins."""

    @classmethod
    def pack_files(cls, files: List[Tuple[str, int]], target_bin_size_bytes: int = 134217728) -> List[CompactionBin]:
        """
        files: list of (file_path, file_size_bytes)
        target_bin_size_bytes: default 128MB (128 * 1024 * 1024)
        """
        if not files:
            return []

        # Sort descending by size (FFD heuristic)
        sorted_files = sorted(files, key=lambda x: x[1], reverse=True)
        bins: List[CompactionBin] = []

        for path, size in sorted_files:
            placed = False
            for b in bins:
                if b.total_size_bytes + size <= target_bin_size_bytes:
                    b.file_paths.append(path)
                    b.total_size_bytes += size
                    placed = True
                    break

            if not placed:
                new_bin = CompactionBin(
                    bin_id=len(bins) + 1,
                    file_paths=[path],
                    total_size_bytes=size
                )
                bins.append(new_bin)

        return bins
