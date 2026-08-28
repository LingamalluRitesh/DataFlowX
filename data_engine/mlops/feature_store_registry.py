"""
DataFlowX Dual Online-Offline Enterprise Feature Store
Provides low-latency Redis/In-Memory online point-lookups and point-in-time correct Lakehouse time-travel joins for ML training.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import pandas as pd
from pydantic import BaseModel, Field


class FeatureView(BaseModel):
    view_name: str
    entity_key: str
    features: List[str] = Field(default_factory=list)
    source_table: str
    online_enabled: bool = True
    ttl_seconds: int = 86400


class FeatureStoreRegistry:
    """Manages online and offline feature retrieval."""

    def __init__(self):
        self.feature_views: Dict[str, FeatureView] = {}
        # Online store: view_name -> entity_key_val -> dict of features
        self.online_store: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def register_view(self, view: FeatureView) -> None:
        self.feature_views[view.view_name] = view
        if view.view_name not in self.online_store:
            self.online_store[view.view_name] = {}

    def ingest_online_features(self, view_name: str, records: List[Dict[str, Any]]) -> int:
        if view_name not in self.feature_views:
            raise ValueError(f"Feature view {view_name} not registered")

        view = self.feature_views[view_name]
        k_col = view.entity_key
        count = 0

        for r in records:
            if k_col in r:
                key_val = str(r[k_col])
                feat_dict = {f: r[f] for f in view.features if f in r}
                self.online_store[view_name][key_val] = feat_dict
                count += 1

        return count

    def get_online_features(self, view_name: str, entity_keys: List[str]) -> List[Dict[str, Any]]:
        if view_name not in self.online_store:
            return []
        v_store = self.online_store[view_name]
        return [{view.entity_key: k, **v_store.get(k, {})} for k in entity_keys for view in [self.feature_views[view_name]]]
