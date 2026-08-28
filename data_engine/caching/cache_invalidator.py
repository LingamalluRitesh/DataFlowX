"""
DataFlowX Tag-Based Lakehouse Version Cache Invalidator
Invalidates cached query results automatically whenever a target table commits a new snapshot version in Delta Lake / Iceberg.
"""

from typing import Dict, List, Set
from backend.core.logging import get_logger

logger = get_logger(__name__)


class CacheInvalidator:
    """Manages table -> cache key dependencies."""

    def __init__(self):
        # table_name -> set of cache_keys
        self._table_to_keys: Dict[str, Set[str]] = {}

    def link_query_to_table(self, cache_key: str, table_name: str) -> None:
        self._table_to_keys.setdefault(table_name.lower(), set()).add(cache_key)

    def invalidate_table_cache(self, table_name: str) -> List[str]:
        keys = list(self._table_to_keys.pop(table_name.lower(), set()))
        logger.info(f"Invalidated {len(keys)} cached query results for table '{table_name}'")
        return keys
