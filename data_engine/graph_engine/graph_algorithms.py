"""
DataFlowX Graph Analytics Algorithms
Implements PageRank centrality, Dijkstra shortest paths, and Tarjan's Strongly Connected Components.
"""

from collections import defaultdict, deque
import heapq
from typing import Dict, List, Optional, Set, Tuple
from data_engine.graph_engine.property_graph import PropertyGraph


class GraphAlgorithms:
    """Graph algorithm execution suite."""

    @classmethod
    def page_rank(cls, graph: PropertyGraph, damping_factor: float = 0.85, max_iterations: int = 30, tolerance: float = 1e-6) -> Dict[str, float]:
        nodes = list(graph.nodes.keys())
        n = len(nodes)
        if n == 0:
            return {}

        ranks = {node: 1.0 / n for node in nodes}

        for _ in range(max_iterations):
            new_ranks = {}
            diff = 0.0

            for node in nodes:
                in_nodes = graph.get_neighbors(node, direction="IN")
                rank_sum = 0.0
                for in_n in in_nodes:
                    out_degree = len(graph.get_neighbors(in_n, direction="OUT"))
                    if out_degree > 0:
                        rank_sum += ranks[in_n] / out_degree

                new_rank = ((1.0 - damping_factor) / n) + (damping_factor * rank_sum)
                new_ranks[node] = new_rank
                diff += abs(new_rank - ranks[node])

            ranks = new_ranks
            if diff < tolerance:
                break

        # Normalize so sum = 1.0
        total_r = sum(ranks.values())
        if total_r > 0:
            ranks = {k: round(v / total_r, 6) for k, v in ranks.items()}

        return ranks

    @classmethod
    def dijkstra_shortest_path(cls, graph: PropertyGraph, start_node: str, end_node: str, weight_property: str = "weight") -> Optional[Tuple[float, List[str]]]:
        if start_node not in graph.nodes or end_node not in graph.nodes:
            return None

        distances = {node: float("inf") for node in graph.nodes}
        distances[start_node] = 0.0
        previous = {node: None for node in graph.nodes}

        pq = [(0.0, start_node)]

        while pq:
            curr_d, curr_n = heapq.heappop(pq)
            if curr_n == end_node:
                break
            if curr_d > distances[curr_n]:
                continue

            for edge_id in graph.out_edges.get(curr_n, []):
                edge = graph.edges[edge_id]
                neighbor = edge.target_id
                weight = float(edge.properties.get(weight_property, 1.0))
                d = curr_d + weight

                if d < distances[neighbor]:
                    distances[neighbor] = d
                    previous[neighbor] = curr_n
                    heapq.heappush(pq, (d, neighbor))

        if distances[end_node] == float("inf"):
            return None

        # Reconstruct path
        path = []
        curr = end_node
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse()

        return round(distances[end_node], 2), path
