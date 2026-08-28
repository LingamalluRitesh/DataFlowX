"""
DataFlowX Inverted File Index with Product Quantization (IVF-PQ)
Combines Voronoi cell coarse clustering with product quantization for billion-scale Lakehouse vector retrieval.
"""

from typing import Dict, List, Tuple
import numpy as np
from data_engine.ann_index.product_quantizer import ProductQuantizer


class IVFPQIndex:
    """IVF-PQ Vector Index."""

    def __init__(self, dim: int = 128, n_clusters: int = 16, m_subvectors: int = 8, n_probe: int = 4):
        self.dim = dim
        self.n_clusters = n_clusters
        self.n_probe = n_probe
        self.pq = ProductQuantizer(dim=dim, m_subvectors=m_subvectors)

        # Coarse centroids: shape (n_clusters, dim)
        np.random.seed(42)
        self.centroids = np.random.randn(n_clusters, dim)
        # Inverted lists: cluster_id -> list of (doc_id, codes)
        self.inverted_lists: Dict[int, List[Tuple[int, List[int]]]] = {c: [] for c in range(n_clusters)}

    def _find_nearest_clusters(self, vec: np.ndarray, top_k: int) -> List[int]:
        dists = np.linalg.norm(self.centroids - vec, axis=1)
        return list(np.argsort(dists)[:top_k])

    def insert(self, doc_id: int, vector: List[float]) -> None:
        arr = np.array(vector, dtype=float)
        cluster_id = self._find_nearest_clusters(arr, top_k=1)[0]
        codes = self.pq.encode(vector)
        self.inverted_lists[cluster_id].append((doc_id, codes))

    def search(self, query_vector: List[float], k: int = 10) -> List[Tuple[int, float]]:
        q_arr = np.array(query_vector, dtype=float)
        probed_clusters = self._find_nearest_clusters(q_arr, top_k=self.n_probe)

        candidates = []
        for c_id in probed_clusters:
            for doc_id, codes in self.inverted_lists[c_id]:
                dist = self.pq.compute_asymmetric_distance(query_vector, codes)
                candidates.append((doc_id, dist))

        candidates.sort(key=lambda x: x[1])
        return [(doc_id, round(1.0 / (1.0 + dist), 4)) for doc_id, dist in candidates[:k]]
