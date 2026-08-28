"""
DataFlowX Bidirectional Lineage Graph Traverser
Executes BFS/DFS graph traversals across dataset lineage dependencies to compute upstream provenance and downstream blast radius.
"""

from collections import deque
from typing import Dict, List, Set
from pydantic import BaseModel, Field


class LineageTraversalNode(BaseModel):
    node_id: str
    node_type: str  # TABLE, VIEW, PIPELINE, MODEL
    depth: int = 0


class LineageGraphTraverser:
    """Traverses directed lineage graphs."""

    def __init__(self, adjacency_list: Dict[str, List[str]]):
        self.adj = adjacency_list

    def get_downstream_impact(self, root_node_id: str, max_depth: int = 10) -> List[LineageTraversalNode]:
        """BFS downstream traversal."""
        visited: Set[str] = {root_node_id}
        queue = deque([(root_node_id, 0)])
        results = []

        while queue:
            curr, d = queue.popleft()
            if d > 0:
                results.append(LineageTraversalNode(node_id=curr, node_type="TABLE", depth=d))
            if d < max_depth:
                for neighbor in self.adj.get(curr, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, d + 1))

        return results

    def get_upstream_provenance(self, reverse_adj: Dict[str, List[str]], target_node_id: str) -> List[str]:
        """Finds all root origin nodes."""
        visited: Set[str] = {target_node_id}
        queue = deque([target_node_id])
        roots = []

        while queue:
            curr = queue.popleft()
            parents = reverse_adj.get(curr, [])
            if not parents and curr != target_node_id:
                roots.append(curr)
            for p in parents:
                if p not in visited:
                    visited.add(p)
                    queue.append(p)

        return roots
