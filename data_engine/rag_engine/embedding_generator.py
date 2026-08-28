"""
DataFlowX Dense Vector Embedding & Cosine Similarity Engine
Generates dense vector embeddings and computes vectorized cosine similarities for hybrid RAG search over Lakehouse unstructured documents.
"""

from typing import List, Optional
import numpy as np


class VectorEmbeddingGenerator:
    """Computes dense vector representations and cosine metrics."""

    @staticmethod
    def compute_cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        a = np.array(vec_a, dtype=float)
        b = np.array(vec_b, dtype=float)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    @classmethod
    def generate_mock_embedding(cls, text: str, dimension: int = 128) -> List[float]:
        # Deterministic vector based on text hash
        import hashlib
        h = hashlib.md5(text.encode("utf-8")).hexdigest()
        np.random.seed(int(h[:8], 16))
        vec = np.random.randn(dimension)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist()
