"""
DataFlowX Columnar Inverted Index & Posting List Engine
Indexes string, tag, and array columns using compressed posting lists for sub-millisecond multi-attribute search filtering.
"""

from typing import Dict, List, Optional, Set
from data_engine.indexing.roaring_bitmap import RoaringBitmap


class ColumnarInvertedIndex:
    """Maintains inverted term -> RoaringBitmap posting lists."""

    def __init__(self, column_name: str):
        self.column_name = column_name
        self.postings: Dict[str, RoaringBitmap] = {}

    def index_row(self, row_id: int, term: str) -> None:
        if not term:
            return
        t_clean = str(term).lower()
        bm = self.postings.setdefault(t_clean, RoaringBitmap())
        bm.add(row_id)

    def lookup_term(self, term: str) -> RoaringBitmap:
        t_clean = str(term).lower()
        return self.postings.get(t_clean, RoaringBitmap())
