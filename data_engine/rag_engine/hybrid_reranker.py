"""
DataFlowX Reciprocal Rank Fusion (RRF) Hybrid Search Reranker
Fuses dense vector k-NN ranks and sparse BM25 keyword ranks into a unified relevance score with k=60 penalty factor.
"""

from typing import Dict, List, Tuple


class HybridRankFusion:
    """Combines dense and sparse search rankings."""

    @classmethod
    def fuse_rankings(cls, dense_ranks: List[int], sparse_ranks: List[int], k: int = 60) -> List[Tuple[int, float]]:
        scores: Dict[int, float] = {}
        for rank, doc_id in enumerate(dense_ranks):
            scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank + 1))

        for rank, doc_id in enumerate(sparse_ranks):
            scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank + 1))

        fused = [(doc_id, round(score, 6)) for doc_id, score in scores.items()]
        return sorted(fused, key=lambda s: s[1], reverse=True)
