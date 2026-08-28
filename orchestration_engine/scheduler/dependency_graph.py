"""
DataFlowX DAG Dependency Graph & Topological Execution Waves
Computes topological waves using Kahn's algorithm, identifies critical path bottlenecks, and validates acyclicity.
"""

from typing import Dict, List, Set, Tuple


class DependencyGraph:
    """Directed Acyclic Graph (DAG) analyzer."""

    def __init__(self):
        self.adj_list: Dict[str, List[str]] = {}  # task -> downstream dependents
        self.in_degree: Dict[str, int] = {}
        self.all_nodes: Set[str] = set()

    def add_node(self, node_id: str) -> None:
        self.all_nodes.add(node_id)
        self.adj_list.setdefault(node_id, [])
        self.in_degree.setdefault(node_id, 0)

    def add_edge(self, upstream_id: str, downstream_id: str) -> None:
        self.add_node(upstream_id)
        self.add_node(downstream_id)
        self.adj_list[upstream_id].append(downstream_id)
        self.in_degree[downstream_id] = self.in_degree.get(downstream_id, 0) + 1

    def compute_execution_waves(self) -> List[List[str]]:
        """Compute parallel execution waves using Kahn's algorithm."""
        in_deg = dict(self.in_degree)
        current_wave = [node for node in self.all_nodes if in_deg[node] == 0]
        waves = []
        visited_count = 0

        while current_wave:
            waves.append(current_wave)
            visited_count += len(current_wave)
            next_wave = []

            for node in current_wave:
                for downstream in self.adj_list.get(node, []):
                    in_deg[downstream] -= 1
                    if in_deg[downstream] == 0:
                        next_wave.append(downstream)

            current_wave = next_wave

        if visited_count < len(self.all_nodes):
            raise ValueError("Dependency cycle detected in DAG")

        return waves
