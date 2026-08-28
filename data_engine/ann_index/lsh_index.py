"""
DataFlowX Locality-Sensitive Hashing (LSH) Random Hyperplane Index
Partitions dense vector spaces into hash buckets using random hyperplanes for constant-time candidate filtering.
"""

from typing import Dict, List, Set, Tuple
import numpy as np


class RandomHyperplaneLSH:
    """LSH Index for cosine similarity."""

    def __init__(self, dim: int = 128, num_bits: int = 16, num_tables: int = 4):
        self.dim = dim
        self.num_bits = num_bits
        self.num_tables = num_tables
        # Generate random projection hyperplanes per table: shape (num_tables, num_bits, dim)
        np.random.seed(42)
        self.hyperplanes = [np.random.randn(num_bits, dim) for _ in range(num_tables)]
        # Buckets: table_idx -> hash_code_int -> list of (doc_id, vector)
        self.tables: List[Dict[int, List[Tuple[int, np.ndarray]]]] = [{} for _ in range(num_tables)]

    def _hash_vector(self, table_idx: int, vec: np.ndarray) -> int:
        projections = np.dot(self.hyperplanes[table_idx], vec)
        bits = (projections >= 0).astype(int)
        code = 0
        for b in bits:
            code = (code << 1) | int(b)
        return code

    def index_vector(self, doc_id: int, vector: List[float]) -> None:
        arr = np.array(vector, dtype=float)
        for t_idx in range(self.num_tables):
            code = self._hash_vector(t_idx, arr)
            if code not in self.tables[t_idx]:
                self.tables[t_idx][code] = []
            self.tables[t_idx][code].append((doc_id, arr))

    def query(self, query_vector: List[float], k: int = 10) -> List[Tuple[int, float]]:
        q_arr = np.array(query_vector, dtype=float)
        candidates: Dict[int, np.ndarray] = {}

        for t_idx in range(self.num_tables):
            code = self._hash_vector(t_idx, q_arr)
            for doc_id, vec in self.tables[t_idx].get(code, []):
                candidates[doc_id] = vec

        if not candidates:
            return []

        scored = []
        q_norm = np.linalg.norm(q_arr)
        for doc_id, vec in candidates.items():
            d_norm = np.linalg.norm(vec)
            sim = float(np.dot(q_arr, vec) / (q_norm * d_norm)) if q_norm > 0 and d_norm > 0 else 0.0
            scored.append((doc_id, round(sim, 4)))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]
