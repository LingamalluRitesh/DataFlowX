"""
DataFlowX Scan-Resistant 2-Segmented LRU (2Q / SLRU) Cache
Maintains probationary (A1in) and protected (Am) segments to prevent large sequential full-table scans from evicting frequently accessed dimension records.
"""

from collections import OrderedDict
from typing import Any, Optional


class SegmentedLRUCache:
    """Scan-resistant 2-segmented LRU cache."""

    def __init__(self, probationary_capacity: int = 500, protected_capacity: int = 500):
        self.probationary_cap = probationary_capacity
        self.protected_cap = protected_capacity
        self.probationary: OrderedDict[str, Any] = OrderedDict()
        self.protected: OrderedDict[str, Any] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        if key in self.protected:
            self.protected.move_to_end(key)
            return self.protected[key]

        if key in self.probationary:
            # Promote to protected segment
            val = self.probationary.pop(key)
            self.protected[key] = val
            if len(self.protected) > self.protected_cap:
                # Demote oldest protected back to probationary
                demoted_k, demoted_v = self.protected.popitem(last=False)
                self.probationary[demoted_k] = demoted_v
                if len(self.probationary) > self.probationary_cap:
                    self.probationary.popitem(last=False)
            return val

        return None

    def put(self, key: str, value: Any) -> None:
        if key in self.protected:
            self.protected[key] = value
            self.protected.move_to_end(key)
            return

        if key in self.probationary:
            self.probationary[key] = value
            self.probationary.move_to_end(key)
            return

        # New entry enters probationary segment
        self.probationary[key] = value
        if len(self.probationary) > self.probationary_cap:
            self.probationary.popitem(last=False)
