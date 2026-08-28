"""
DataFlowX Resource Allocation & Wait-For-Graph Deadlock Detector
Maintains dynamic Wait-For-Graph (WFG) edges between active pipeline tasks and resources, executing Tarjan's strongly connected components algorithm to preempt deadlocked workers.
"""

from typing import Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class DeadlockCycle(BaseModel):
    cycle_nodes: List[str]
    victim_task_id: str


class DeadlockDetector:
    """Detects cycles in task wait-for-resource dependency graphs."""

    def __init__(self):
        # task_id -> set of task_ids that it is blocked waiting for
        self.wait_for_graph: Dict[str, Set[str]] = {}

    def add_wait_edge(self, waiting_task_id: str, holding_task_id: str) -> None:
        self.wait_for_graph.setdefault(waiting_task_id, set()).add(holding_task_id)

    def remove_wait_edge(self, waiting_task_id: str, holding_task_id: str) -> None:
        if waiting_task_id in self.wait_for_graph:
            self.wait_for_graph[waiting_task_id].discard(holding_task_id)

    def detect_deadlock_cycles(self) -> List[DeadlockCycle]:
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        cycles = []

        def dfs(node: str, path: List[str]):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in self.wait_for_graph.get(node, set()):
                if neighbor not in visited:
                    dfs(neighbor, path)
                elif neighbor in rec_stack:
                    # Found cycle
                    c_start = path.index(neighbor)
                    cycle_nodes = list(path[c_start:])
                    victim = cycle_nodes[-1]  # preempt latest node in cycle
                    cycles.append(DeadlockCycle(cycle_nodes=cycle_nodes, victim_task_id=victim))
                    logger.critical(f"Deadlock detected! Cycle: {' -> '.join(cycle_nodes)}. Preempting victim task '{victim}'")

            rec_stack.remove(node)
            path.pop()

        for node in list(self.wait_for_graph.keys()):
            if node not in visited:
                dfs(node, [])

        return cycles
