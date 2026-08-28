"""
DataFlowX Parquet Bin-Packing Small File Optimizer
Implements First-Fit Decreasing (FFD) bin-packing algorithm to merge fragmented small Parquet files into target 128MB or 256MB Lakehouse chunks.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ParquetFileDescriptor(BaseModel):
    file_path: str
    size_bytes: int
    record_count: int


class CompactionBin(BaseModel):
    bin_id: int
    target_size_bytes: int
    current_size_bytes: int = 0
    files: List[ParquetFileDescriptor] = Field(default_factory=list)


class BinPackingCompactor:
    """Groups small files into target size bins."""

    @classmethod
    def pack_files(cls, files: List[ParquetFileDescriptor], target_bin_size_bytes: int = 134217728) -> List[CompactionBin]:
        """First-Fit Decreasing algorithm."""
        sorted_files = sorted(files, key=lambda f: f.size_bytes, reverse=True)
        bins: List[CompactionBin] = []

        for f in sorted_files:
            placed = False
            for b in bins:
                if b.current_size_bytes + f.size_bytes <= target_bin_size_bytes:
                    b.files.append(f)
                    b.current_size_bytes += f.size_bytes
                    placed = True
                    break
            if not placed:
                new_bin = CompactionBin(bin_id=len(bins), target_size_bytes=target_bin_size_bytes, current_size_bytes=f.size_bytes, files=[f])
                bins.append(new_bin)

        return bins
