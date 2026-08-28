"""
DataFlowX Vector Product Quantization (PQ) Codebook Compressor
Compresses floating point vector embeddings into compact byte-codes using sub-vector k-means quantization.
"""

from typing import List, Tuple
import numpy as np


class ProductQuantizer:
    """Product Quantizer for memory compression."""

    def __init__(self, dim: int = 128, m_subvectors: int = 8, k_centroids: int = 256):
        self.dim = dim
        self.m = m_subvectors
        self.d_sub = dim // m_subvectors
        self.k = k_centroids
        # Codebooks: shape (m, k, d_sub)
        np.random.seed(42)
        self.codebooks = np.random.randn(self.m, self.k, self.d_sub)

    def encode(self, vector: List[float]) -> List[int]:
        """Encodes vector into m-byte integer code."""
        arr = np.array(vector, dtype=float)
        codes = []
        for i in range(self.m):
            sub_vec = arr[i * self.d_sub:(i + 1) * self.d_sub]
            # Find closest centroid in codebook i
            dists = np.linalg.norm(self.codebooks[i] - sub_vec, axis=1)
            best_idx = int(np.argmin(dists))
            codes.append(best_idx)
        return codes

    def decode(self, codes: List[int]) -> np.ndarray:
        """Reconstructs approximate vector from codes."""
        parts = []
        for i, code in enumerate(codes):
            parts.append(self.codebooks[i][code])
        return np.concatenate(parts)

    def compute_asymmetric_distance(self, query_vec: List[float], codes: List[int]) -> float:
        """Computes asymmetric distance between unquantized query and quantized vector."""
        q_arr = np.array(query_vec, dtype=float)
        total_dist_sq = 0.0
        for i, code in enumerate(codes):
            q_sub = q_arr[i * self.d_sub:(i + 1) * self.d_sub]
            c_sub = self.codebooks[i][code]
            total_dist_sq += float(np.sum((q_sub - c_sub) ** 2))
        return float(np.sqrt(total_dist_sq))
