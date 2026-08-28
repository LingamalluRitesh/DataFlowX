"""
DataFlowX Hierarchical Navigable Small World (HNSW) Vector Graph Index
Implements multi-layer HNSW graph indexing for sub-millisecond approximate nearest neighbor (ANN) vector searches over embeddings.
"""

import math
import random
from typing import Dict, List, Optional, Set, Tuple
import numpy as np


class HNSWNode:
    def __init__(self, node_id: int, vector: List[float], level: int):
        self.node_id = node_id
        self.vector = np.array(vector, dtype=float)
        self.level = level
        # neighbors per layer: layer_idx -> set of node_ids
        self.neighbors: Dict[int, Set[int]] = {l: set() for l in range(level + 1)}


class HNSWIndex:
    """HNSW vector index."""

    def __init__(self, dim: int = 128, m: int = 16, ef_construction: int = 64, ml: Optional[float] = None):
        self.dim = dim
        self.m = m
        self.m_max0 = m * 2
        self.ef_construction = ef_construction
        self.ml = ml if ml is not None else 1.0 / math.log(m)
        self.nodes: Dict[int, HNSWNode] = {}
        self.entry_point_id: Optional[int] = None
        self.max_level = -1

    @staticmethod
    def _cosine_dist(a: np.ndarray, b: np.ndarray) -> float:
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 1.0
        return 1.0 - float(np.dot(a, b) / (norm_a * norm_b))

    def _random_level(self) -> int:
        r = random.random()
        lvl = int(-math.log(max(1e-9, r)) * self.ml)
        return min(lvl, 16)

    def insert(self, node_id: int, vector: List[float]) -> None:
        lvl = self._random_level()
        new_node = HNSWNode(node_id, vector, lvl)
        self.nodes[node_id] = new_node

        if self.entry_point_id is None:
            self.entry_point_id = node_id
            self.max_level = lvl
            return

        curr_obj = self.nodes[self.entry_point_id]
        curr_dist = self._cosine_dist(new_node.vector, curr_obj.vector)

        # 1. Search nearest entry point from top level down to lvl+1
        for lc in range(self.max_level, lvl, -1):
            changed = True
            while changed:
                changed = False
                for neighbor_id in curr_obj.neighbors.get(lc, []):
                    n_node = self.nodes[neighbor_id]
                    d = self._cosine_dist(new_node.vector, n_node.vector)
                    if d < curr_dist:
                        curr_dist = d
                        curr_obj = n_node
                        changed = True

        # 2. For layers from min(max_level, lvl) down to 0, connect neighbors
        for lc in range(min(self.max_level, lvl), -1, -1):
            candidates = self._search_layer(new_node.vector, curr_obj, self.ef_construction, lc)
            # Select m nearest neighbors
            selected = sorted(candidates, key=lambda x: x[0])[:self.m]
            for dist, n_node in selected:
                new_node.neighbors[lc].add(n_node.node_id)
                n_node.neighbors[lc].add(node_id)
                # Prune if exceeding max neighbors
                max_m = self.m_max0 if lc == 0 else self.m
                if len(n_node.neighbors[lc]) > max_m:
                    n_neighbors = [(self._cosine_dist(n_node.vector, self.nodes[nid].vector), nid) for nid in n_node.neighbors[lc]]
                    n_neighbors.sort()
                    n_node.neighbors[lc] = {nid for _, nid in n_neighbors[:max_m]}

        if lvl > self.max_level:
            self.max_level = lvl
            self.entry_point_id = node_id

    def _search_layer(self, query_vec: np.ndarray, ep: HNSWNode, ef: int, lc: int) -> List[Tuple[float, HNSWNode]]:
        v_dist = self._cosine_dist(query_vec, ep.vector)
        visited = {ep.node_id}
        candidates = [(v_dist, ep)]
        w = [(v_dist, ep)]

        while candidates:
            c_dist, c_node = candidates.pop(0)
            f_dist = max(w, key=lambda x: x[0])[0] if len(w) >= ef else float("inf")
            if c_dist > f_dist:
                break

            for n_id in c_node.neighbors.get(lc, []):
                if n_id not in visited:
                    visited.add(n_id)
                    n_node = self.nodes[n_id]
                    d = self._cosine_dist(query_vec, n_node.vector)
                    f_dist = max(w, key=lambda x: x[0])[0] if len(w) >= ef else float("inf")
                    if d < f_dist or len(w) < ef:
                        candidates.append((d, n_node))
                        candidates.sort(key=lambda x: x[0])
                        w.append((d, n_node))
                        if len(w) > ef:
                            w.sort(key=lambda x: x[0])
                            w.pop()

        return w

    def search_knn(self, query_vector: List[float], k: int = 10, ef_search: int = 32) -> List[Tuple[int, float]]:
        """Returns top-k (node_id, similarity_score)."""
        if self.entry_point_id is None:
            return []

        q_vec = np.array(query_vector, dtype=float)
        curr_obj = self.nodes[self.entry_point_id]
        curr_dist = self._cosine_dist(q_vec, curr_obj.vector)

        # Traverse down to level 0
        for lc in range(self.max_level, 0, -1):
            changed = True
            while changed:
                changed = False
                for neighbor_id in curr_obj.neighbors.get(lc, []):
                    n_node = self.nodes[neighbor_id]
                    d = self._cosine_dist(q_vec, n_node.vector)
                    if d < curr_dist:
                        curr_dist = d
                        curr_obj = n_node
                        changed = True

        candidates = self._search_layer(q_vec, curr_obj, ef_search, 0)
        sorted_candidates = sorted(candidates, key=lambda x: x[0])[:k]
        # Return (node_id, cosine_similarity = 1 - dist)
        return [(node.node_id, round(1.0 - dist, 4)) for dist, node in sorted_candidates]
