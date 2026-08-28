"""
DataFlowX Range Partition Shard Router
Routes discrete numerical/lexicographical key intervals to designated shard servers, supporting dynamic split and merge partition operations.
"""

from typing import List, Optional
from pydantic import BaseModel


class ShardRange(BaseModel):
    shard_id: str
    min_key: str
    max_key: str
    node_id: str


class RangePartitionRouter:
    """Routes continuous key ranges to storage shards."""

    def __init__(self, shards: List[ShardRange]):
        self.shards = sorted(shards, key=lambda s: s.min_key)

    def route_key(self, key: str) -> Optional[str]:
        for s in self.shards:
            if s.min_key <= key <= s.max_key:
                return s.node_id
        return None
