"""
DataFlowX Consistent Hashing Ring with Virtual Nodes
Distributes partition keys uniformly across worker nodes using 256 virtual nodes (vnodes) per node to minimize reshuffling upon cluster scale up/down.
"""

import bisect
import hashlib
from typing import Dict, List, Optional


class ConsistentHashRing:
    """Consistent hash ring with virtual nodes."""

    def __init__(self, vnodes: int = 256):
        self.vnodes = vnodes
        self.ring: List[int] = []
        self.vnode_to_node: Dict[int, str] = {}

    @staticmethod
    def _hash(key: str) -> int:
        return int(hashlib.md5(key.encode("utf-8")).hexdigest()[:8], 16)

    def add_node(self, node_id: str) -> None:
        for i in range(self.vnodes):
            v_key = f"{node_id}#vnode_{i}"
            h = self._hash(v_key)
            bisect.insort(self.ring, h)
            self.vnode_to_node[h] = node_id

    def get_node(self, partition_key: str) -> Optional[str]:
        if not self.ring:
            return None
        h = self._hash(partition_key)
        idx = bisect.bisect_right(self.ring, h)
        if idx == len(self.ring):
            idx = 0
        return self.vnode_to_node[self.ring[idx]]
