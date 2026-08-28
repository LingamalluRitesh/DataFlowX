"""
DataFlowX Hybrid Semantic & Lexical Catalog Search Engine
Combines dense vector HNSW nearest-neighbor retrieval with sparse BM25 keyword matching via Reciprocal Rank Fusion (RRF).
"""

from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from backend.core.logging import get_logger
from data_engine.vector.hnsw_index import HNSWIndex
from data_engine.vector.tokenizer_embedder import BM25OkapiIndexer, TextTokenizerEmbedder

logger = get_logger(__name__)


class SearchHit(BaseModel):
    asset_id: str
    combined_score: float
    bm25_score: float
    vector_distance: float
    metadata: Dict[str, Any] = Field(default_factory=dict)


class HybridSemanticSearchEngine:
    """Enterprise Search Engine for Data Catalog Assets and Schemas."""

    def __init__(self, vector_dim: int = 128):
        self.embedder = TextTokenizerEmbedder(vector_dim=vector_dim)
        self.hnsw = HNSWIndex(dim=vector_dim, metric="cosine")
        self.bm25 = BM25OkapiIndexer()
        self.metadata_store: Dict[str, Dict[str, Any]] = {}

    def index_asset(self, asset_id: str, title: str, description: str, tags: List[str], metadata: Optional[Dict[str, Any]] = None) -> None:
        full_text = f"{title} {description} {' '.join(tags)}"
        meta = metadata or {}
        meta.update({"title": title, "description": description, "tags": tags})
        self.metadata_store[asset_id] = meta

        # 1. Index in BM25
        self.bm25.add_document(asset_id, full_text)

        # 2. Index in HNSW
        emb = self.embedder.text_to_embedding(full_text)
        self.hnsw.insert(asset_id, emb, meta)

    def hybrid_search(self, query: str, top_k: int = 10, rrf_k: int = 60) -> List[SearchHit]:
        """Reciprocal Rank Fusion of BM25 and Vector ANN."""
        bm25_results = self.bm25.score_query(query)
        bm25_ranks = {doc_id: rank for rank, (score, doc_id) in enumerate(bm25_results, start=1)}
        bm25_scores = {doc_id: score for score, doc_id in bm25_results}

        q_vec = self.embedder.text_to_embedding(query)
        vector_results = self.hnsw.search(q_vec, top_k=top_k * 2)
        vector_ranks = {nid: rank for rank, (dist, nid, meta) in enumerate(vector_results, start=1)}
        vector_dists = {nid: dist for dist, nid, meta in vector_results}

        all_doc_ids = set(bm25_ranks.keys()).union(set(vector_ranks.keys()))
        fused_scores = {}

        for doc_id in all_doc_ids:
            score = 0.0
            if doc_id in bm25_ranks:
                score += 1.0 / (rrf_k + bm25_ranks[doc_id])
            if doc_id in vector_ranks:
                score += 1.0 / (rrf_k + vector_ranks[doc_id])
            fused_scores[doc_id] = score

        sorted_docs = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        hits = []
        for doc_id, c_score in sorted_docs:
            hits.append(SearchHit(
                asset_id=doc_id,
                combined_score=round(c_score, 6),
                bm25_score=bm25_scores.get(doc_id, 0.0),
                vector_distance=vector_dists.get(doc_id, 1.0),
                metadata=self.metadata_store.get(doc_id, {})
            ))

        return hits
