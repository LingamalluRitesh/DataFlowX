"""
DataFlowX Feature Store Service Layer
Coordinates feature view registration, point-in-time offline training joins, and low-latency online serving.
"""

from typing import Any, Dict, List, Optional
import pandas as pd
from data_engine.feature_store.drift_monitor import FeatureDriftMonitor, FeatureDriftReport
from data_engine.feature_store.feature_view import FeatureDefinition, FeatureView
from data_engine.feature_store.online_serving import OnlineFeatureStore


class FeatureStoreService:
    """Service layer for ML feature views."""

    def __init__(self):
        self.views: Dict[str, FeatureView] = {}
        self.online_store = OnlineFeatureStore()

    def register_feature_view(self, view: FeatureView) -> FeatureView:
        self.views[view.name] = view
        return view

    def list_feature_views(self) -> List[FeatureView]:
        return list(self.views.values())

    def get_online_features(self, view_name: str, entity_ids: List[str]) -> List[Dict[str, Any]]:
        return self.online_store.get_online_features(view_name, entity_ids)
