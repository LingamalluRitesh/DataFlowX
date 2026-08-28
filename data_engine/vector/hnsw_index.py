"""
DataFlowX Hierarchical Navigable Small World (HNSW) Vector Index
Pure Python implementation of approximate nearest neighbor (ANN) search graph with multi-layer skip-lists and cosine/Euclidean distance metrics for high-dimensional schema embeddings.
"""

import heapq
import math
import random
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import numpy as np
from pydantic import BaseModel, Field


def cosine_distance(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine distance (1.0 - cosine_similarity)."""
    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0
    for a, b in zip(vec_a, vec_b):
        dot += a * b
        norm_a += a * a
        norm_b += b * b
    if norm_a == 0.0 or norm_b == 0.0:
        return 1.0
    sim = dot / (math.sqrt(norm_a) * math.sqrt(norm_b))
    return max(0.0, 1.0 - sim)


def euclidean_distance(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute L2 Euclidean distance."""
    s = 0.0
    for a, b in zip(vec_a, vec_b):
        diff = a - b
        s += diff * diff
    return math.sqrt(s)


class HNSWNode(BaseModel):
    node_id: str
    vector: List[float]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    # layer_idx -> list of neighbor node_ids
    neighbors: Dict[int, List[str]] = Field(default_factory=dict)


class HNSWIndex:
    """Multi-layer approximate nearest neighbor graph index."""

    def __init__(self, dim: int = 128, m: int = 16, ef_construction: int = 64, metric: str = "cosine"):
        self.dim = dim
        self.m = m  # max outgoing connections per node
        self.m0 = 2 * m  # max connections at bottom layer 0
        self.ef_construction = ef_construction
        self.metric = metric
        self.distance_fn = cosine_distance if metric == "cosine" else euclidean_distance
        self.nodes: Dict[str, HNSWNode] = {}
        self.entry_point_id: Optional[str] = None
        self.max_layer: int = -1
        self.mult = 1.0 / math.log(m)

    def _random_level(self) -> int:
        r = random.random()
        if r == 0:
            r = 0.0000001
        return int(-math.log(r) * self.mult)

    def insert(self, node_id: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None) -> None:
        """Insert vector item into HNSW graph."""
        if len(vector) != self.dim:
            raise ValueError(f"Vector dim {len(vector)} does not match index dim {self.dim}")

        target_level = self._random_level()
        node = HNSWNode(node_id=node_id, vector=vector, metadata=metadata or {}, neighbors={l: [] for l in range(target_level + 1)})
        self.nodes[node_id] = node

        if self.entry_point_id is None:
            self.entry_point_id = node_id
            self.max_layer = target_level
            return

        curr_ep = self.entry_point_id

        # 1. Greedy search down to target_level
        for level in range(self.max_layer, target_level, -1):
            curr_ep = self._search_layer_closest(curr_ep, vector, level)

        # 2. Search and connect for levels <= target_level
        for level in range(min(self.max_layer, target_level), -1, -1):
            candidates = self._search_layer_candidates(curr_ep, vector, self.ef_construction, level)
            # Pick M closest neighbors
            max_m = self.m0 if level == 0 else self.m
            neighbors = [cand_id for dist, cand_id in candidates[:max_m]]
            node.neighbors[level] = neighbors

            # Add reverse connections
            for neighbor_id in neighbors:
                n_node = self.nodes[neighbor_id]
                if level in n_node.neighbors:
                    n_node.neighbors[level].append(node_id)
                    # Prune if exceeding max_m
                    if len(n_node.neighbors[level]) > max_m:
                        n_node.neighbors[level] = n_node.neighbors[level][:max_m]

            curr_ep = candidates[0][1] if candidates else curr_ep

        if target_level > self.max_layer:
            self.max_layer = target_level
            self.entry_point_id = node_id

    def search(self, query_vec: List[float], top_k: int = 10, ef_search: int = 32) -> List[Tuple[float, str, Dict[str, Any]]]:
        """Query top_k approximate nearest neighbors."""
        if not self.nodes or self.entry_point_id is None:
            return []

        curr_ep = self.entry_point_id
        for level in range(self.max_layer, 0, -1):
            curr_ep = self._search_layer_closest(curr_ep, query_vec, level)

        candidates = self._search_layer_candidates(curr_ep, query_vec, max(ef_search, top_k), 0)
        results = []
        for dist, nid in candidates[:top_k]:
            results.append((dist, nid, self.nodes[nid].metadata))
        return results

    def _search_layer_closest(self, curr_ep: str, query_vec: List[float], level: int) -> str:
        curr_dist = self.distance_fn(query_vec, self.nodes[curr_ep].vector)
        improved = True
        while improved:
            improved = False
            for neighbor_id in self.nodes[curr_ep].neighbors.get(level, []):
                dist = self.distance_fn(query_vec, self.nodes[neighbor_id].vector)
                if dist < curr_dist:
                    curr_dist = dist
                    curr_ep = neighbor_id
                    improved = True
        return curr_ep

    def _search_layer_candidates(self, curr_ep: str, query_vec: List[float], ef: int, level: int) -> List[Tuple[float, str]]:
        visited = {curr_ep}
        dist = self.distance_fn(query_vec, self.nodes[curr_ep].vector)
        candidates = [(dist, curr_ep)]  # min-heap
        w = [(dist, curr_ep)]  # sorted result list

        while candidates:
            c_dist, c_id = heapq.heappop(candidates)
            if c_dist > w[-1][0] and len(w) >= ef:
                break

            for neighbor_id in self.nodes[c_id].neighbors.get(level, []):
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    n_dist = self.distance_fn(query_vec, self.nodes[neighbor_id].vector)
                    if n_dist < w[-1][0] or len(w) < ef:
                        heapq.heappush(candidates, (n_dist, neighbor_id))
                        w.append((n_dist, neighbor_id))
                        w.sort(key=lambda x: x[0])
                        if len(w) > ef:
                            w.pop()

        return w
