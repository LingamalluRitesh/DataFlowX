"""
DataFlowX Parameterized Query Result Cache Manager
Hashes normalized SQL AST statements and bind parameters into SHA256 cache keys to return instant query responses.
"""

import hashlib
import json
from typing import Any, Dict, Optional
import pandas as pd
from data_engine.caching.lru_cache import ThreadSafeLRUCache


class QueryResultCacheManager:
    """Manages execution result caching."""

    def __init__(self):
        self._cache = ThreadSafeLRUCache()

    @staticmethod
    def compute_cache_key(sql_query: str, params: Optional[Dict[str, Any]] = None) -> str:
        norm_sql = " ".join(sql_query.strip().lower().split())
        param_str = json.dumps(params or {}, sort_keys=True)
        raw = f"{norm_sql}::{param_str}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def get_result(self, cache_key: str) -> Optional[pd.DataFrame]:
        return self._cache.get(cache_key)

    def put_result(self, cache_key: str, df: pd.DataFrame, ttl_seconds: int = 300) -> None:
        self._cache.put(cache_key, df, ttl_seconds=ttl_seconds)
