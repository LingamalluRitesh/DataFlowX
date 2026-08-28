"""
DataFlowX Directed Acyclic Graph (DAG) Engine & Validator
Implements Tarjan's and Kahn's algorithms for cycle detection, topological sorting, dependency resolution, and graph validation.
"""

from collections import defaultdict, deque
from typing import Dict, List, Optional, Set, Tuple
from backend.core.exceptions import DAGCycleError, DAGValidationError
from backend.core.logging import get_logger
from orchestration_engine.dag.models import DAGDefinition, DAGEdge, DAGNode

logger = get_logger(__name__)


class DAGParser:
    """Parser, validator, and topological compiler for pipeline DAGs."""

    def __init__(self, dag_definition: DAGDefinition):
        self.dag = dag_definition
        self.nodes_by_id: Dict[str, DAGNode] = {n.id: n for n in self.dag.nodes}
        self.adj_list: Dict[str, List[str]] = defaultdict(list)
        self.reverse_adj_list: Dict[str, List[str]] = defaultdict(list)
        self.in_degree: Dict[str, int] = {n.id: 0 for n in self.dag.nodes}
        self._build_graph()

    def _build_graph(self) -> None:
        for edge in self.dag.edges:
            src = edge.source
            tgt = edge.target
            if src in self.nodes_by_id and tgt in self.nodes_by_id:
                self.adj_list[src].append(tgt)
                self.reverse_adj_list[tgt].append(src)
                self.in_degree[tgt] = self.in_degree.get(tgt, 0) + 1

    def validate_dag(self) -> Tuple[bool, List[str], List[str]]:
        """
        Validate DAG topology:
        - Check for invalid node references in edges
        - Detect cycles via Kahn's algorithm
        - Identify isolated disconnected nodes
        Returns: (is_valid, errors, warnings)
        """
        errors: List[str] = []
        warnings: List[str] = []

        if not self.dag.nodes:
            errors.append("Pipeline DAG must contain at least one node")
            return False, errors, warnings

        # Validate edge endpoint references
        for edge in self.dag.edges:
            if edge.source not in self.nodes_by_id:
                errors.append(f"Edge references non-existent source node '{edge.source}'")
            if edge.target not in self.nodes_by_id:
                errors.append(f"Edge references non-existent target node '{edge.target}'")
            if edge.source == edge.target:
                errors.append(f"Self-loop cycle detected on node '{edge.source}'")

        if errors:
            return False, errors, warnings

        # Cycle detection via topological sort
        is_cyclic, cycle_nodes = self.detect_cycles()
        if is_cyclic:
            errors.append(f"Circular dependency cycle detected among nodes: {cycle_nodes}")
            return False, errors, warnings

        # Check for isolated nodes if multiple nodes exist
        if len(self.dag.nodes) > 1:
            for node_id in self.nodes_by_id:
                if not self.adj_list[node_id] and not self.reverse_adj_list[node_id]:
                    warnings.append(f"Node '{node_id}' ({self.nodes_by_id[node_id].name}) is isolated and has no connections")

        return True, errors, warnings

    def detect_cycles(self) -> Tuple[bool, List[str]]:
        """Kahn's Algorithm for cycle detection."""
        in_deg = dict(self.in_degree)
        queue = deque([n for n, deg in in_deg.items() if deg == 0])
        visited_count = 0

        while queue:
            node = queue.popleft()
            visited_count += 1
            for neighbor in self.adj_list[node]:
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)

        if visited_count != len(self.nodes_by_id):
            # Find nodes involved in cycle
            cycle_nodes = [n for n, deg in in_deg.items() if deg > 0]
            return True, cycle_nodes
        return False, []

    def get_topological_sort(self) -> List[str]:
        """Return linear execution order of nodes respecting dependencies."""
        is_valid, errors, _ = self.validate_dag()
        if not is_valid:
            raise DAGValidationError(f"Cannot sort invalid DAG: {'; '.join(errors)}", errors)

        in_deg = dict(self.in_degree)
        queue = deque([n for n, deg in in_deg.items() if deg == 0])
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in self.adj_list[node]:
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)

        return order

    def get_execution_layers(self) -> List[List[str]]:
        """
        Group nodes into parallel execution layers/stages where all nodes
        in layer K can be executed concurrently once layer K-1 completes.
        """
        top_order = self.get_topological_sort()
        node_depth: Dict[str, int] = {}

        for node in top_order:
            parents = self.reverse_adj_list[node]
            if not parents:
                node_depth[node] = 0
            else:
                node_depth[node] = max(node_depth[p] for p in parents) + 1

        layers_map: Dict[int, List[str]] = defaultdict(list)
        for node, depth in node_depth.items():
            layers_map[depth].append(node)

        max_depth = max(layers_map.keys()) if layers_map else -1
        return [layers_map[d] for d in range(max_depth + 1)]

    def get_upstream_dependencies(self, node_id: str) -> List[str]:
        """Return direct parent nodes that this node depends on."""
        return self.reverse_adj_list.get(node_id, [])

    def get_downstream_dependents(self, node_id: str) -> List[str]:
        """Return direct child nodes that depend on this node."""
        return self.adj_list.get(node_id, [])
