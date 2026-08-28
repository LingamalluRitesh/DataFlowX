"""
DataFlowX Batched Vector Embedding Inference Worker
Executes batched neural text embedding inference pipelines with micro-batching queues and normalization.
"""

import hashlib
from typing import List, Tuple
import numpy as np


class EmbeddingInferenceWorker:
    """Generates normalized vector embeddings from input text streams."""

    def __init__(self, embedding_dim: int = 128):
        self.embedding_dim = embedding_dim

    def embed_text(self, text: str) -> List[float]:
        """Deterministic feature hashing embedding emulator."""
        h = hashlib.sha256(text.encode("utf-8")).digest()
        vec = []
        for i in range(self.embedding_dim):
            byte_val = h[i % len(h)]
            vec.append((float(byte_val) / 128.0) - 1.0)

        arr = np.array(vec, dtype=float)
        norm = np.linalg.norm(arr)
        if norm > 0:
            arr = arr / norm
        return list(np.round(arr, 6))

    def batch_embed(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        a = np.array(v1, dtype=float)
        b = np.array(v2, dtype=float)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))
