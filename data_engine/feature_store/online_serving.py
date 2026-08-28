"""
DataFlowX Low-Latency Online Feature Serving Store
In-memory key-value cache providing sub-5ms feature vector lookups by entity ID for real-time model inference.
"""

import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class OnlineFeatureRecord(BaseModel):
    entity_id: str
    feature_values: Dict[str, Any]
    last_updated_unix: float


class OnlineFeatureStore:
    """In-memory key-value store for online feature serving."""

    def __init__(self):
        # view_name -> entity_id -> OnlineFeatureRecord
        self._store: Dict[str, Dict[str, OnlineFeatureRecord]] = {}

    def write_features(self, view_name: str, entity_id: str, feature_values: Dict[str, Any]) -> None:
        view_map = self._store.setdefault(view_name, {})
        view_map[entity_id] = OnlineFeatureRecord(
            entity_id=entity_id,
            feature_values=feature_values,
            last_updated_unix=time.time()
        )

    def get_online_features(self, view_name: str, entity_ids: List[str]) -> List[Dict[str, Any]]:
        view_map = self._store.get(view_name, {})
        results = []
        for eid in entity_ids:
            if eid in view_map:
                results.append({"entity_id": eid, **view_map[eid].feature_values})
            else:
                results.append({"entity_id": eid})
        return results
