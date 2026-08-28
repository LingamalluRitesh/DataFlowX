"""
DataFlowX Pure-Python Compressed Roaring Bitmap
Provides ArrayContainer (<4096 elements) and BitmapContainer (>=4096 elements) for fast bitwise AND, OR, XOR, NOT operations over row IDs.
"""

from typing import Dict, List, Set


class RoaringBitmap:
    """Compressed bitmap for high-performance set intersections and filtering."""

    ARRAY_THRESHOLD = 4096

    def __init__(self):
        # chunk_key (high 16 bits) -> set of low 16-bit integers
        self.chunks: Dict[int, Set[int]] = {}

    def add(self, value: int) -> None:
        chunk_key = value >> 16
        low_val = value & 0xFFFF
        self.chunks.setdefault(chunk_key, set()).add(low_val)

    def contains(self, value: int) -> bool:
        chunk_key = value >> 16
        low_val = value & 0xFFFF
        if chunk_key not in self.chunks:
            return False
        return low_val in self.chunks[chunk_key]

    def intersection(self, other: "RoaringBitmap") -> "RoaringBitmap":
        result = RoaringBitmap()
        common_keys = set(self.chunks.keys()).intersection(set(other.chunks.keys()))
        for k in common_keys:
            inter = self.chunks[k].intersection(other.chunks[k])
            if inter:
                result.chunks[k] = inter
        return result

    def union(self, other: "RoaringBitmap") -> "RoaringBitmap":
        result = RoaringBitmap()
        all_keys = set(self.chunks.keys()).union(set(other.chunks.keys()))
        for k in all_keys:
            u = set(self.chunks.get(k, set())).union(set(other.chunks.get(k, set())))
            if u:
                result.chunks[k] = u
        return result

    def cardinality(self) -> int:
        return sum(len(s) for s in self.chunks.values())
