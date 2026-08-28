"""
DataFlowX Watermark State Tracker
Tracks incremental extraction cursors, timestamps, and monotonic IDs to prevent duplicate ingestion.
"""

from datetime import datetime, timezone
import json
import os
from typing import Any, Dict, Optional
from backend.core.logging import get_logger

logger = get_logger(__name__)


class WatermarkTracker:
    """Manages high-watermark state for incremental data pipelines."""

    def __init__(self, state_file: str = "./storage/temp/watermarks.json"):
        self.state_file = os.path.abspath(state_file)
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        self._cache: Dict[str, Any] = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load watermark state: {e}")
        return {}

    def _save_state(self) -> None:
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(self._cache, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to persist watermark state: {e}")

    def get_watermark(self, pipeline_id: str, source_id: str, table_or_target: str) -> Optional[Any]:
        """Retrieve the last processed watermark value."""
        key = f"{pipeline_id}:{source_id}:{table_or_target}"
        return self._cache.get(key)

    def set_watermark(self, pipeline_id: str, source_id: str, table_or_target: str, watermark_value: Any) -> None:
        """Update and commit the latest watermark value."""
        key = f"{pipeline_id}:{source_id}:{table_or_target}"
        self._cache[key] = {
            "value": watermark_value,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        self._save_state()

    def clear_watermark(self, pipeline_id: str, source_id: str, table_or_target: str) -> None:
        """Reset watermark to trigger a full re-ingestion."""
        key = f"{pipeline_id}:{source_id}:{table_or_target}"
        if key in self._cache:
            del self._cache[key]
            self._save_state()
