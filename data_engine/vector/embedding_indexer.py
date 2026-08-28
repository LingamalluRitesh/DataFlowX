"""
DataFlowX Semantic Schema Search & Vector Indexer
Generates TF-IDF / term vector representations for catalog columns and tables to power natural language dataset discovery.
"""

import math
import re
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class VectorSearchResult(BaseModel):
    asset_id: str
    asset_name: str
    score: float
    matched_columns: List[str] = Field(default_factory=list)


class SemanticCatalogIndexer:
    """In-memory vector search engine for data catalog schema discovery."""

    def __init__(self):
        self._doc_tokens: Dict[str, Set[str]] = {}
        self._doc_meta: Dict[str, Dict[str, Any]] = {}

    def index_asset(self, asset_id: str, name: str, description: str, column_names: List[str]) -> None:
        raw_text = f"{name} {description} {' '.join(column_names)}".lower()
        tokens = set(re.findall(r"\b\w+\b", raw_text))
        self._doc_tokens[asset_id] = tokens
        self._doc_meta[asset_id] = {
            "name": name,
            "description": description,
            "columns": column_names
        }

    def search(self, query: str, top_k: int = 5) -> List[VectorSearchResult]:
        q_tokens = set(re.findall(r"\b\w+\b", query.lower()))
        if not q_tokens:
            return []

        results = []
        for doc_id, d_tokens in self._doc_tokens.items():
            intersection = q_tokens.intersection(d_tokens)
            if intersection:
                score = round(len(intersection) / len(q_tokens), 2)
                matched_cols = [c for c in self._doc_meta[doc_id]["columns"] if any(t in c.lower() for t in q_tokens)]
                results.append(VectorSearchResult(
                    asset_id=doc_id,
                    asset_name=self._doc_meta[doc_id]["name"],
                    score=score,
                    matched_columns=matched_cols
                ))

        return sorted(results, key=lambda r: r.score, reverse=True)[:top_k]
