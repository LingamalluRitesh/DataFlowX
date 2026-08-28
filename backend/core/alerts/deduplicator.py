"""
DataFlowX Alert Deduplication & Storm Prevention Engine
Generates cryptographic alert fingerprints and applies token-bucket / sliding window suppressions to prevent alert fatigue.
"""

import hashlib
import time
from typing import Dict
from backend.core.alerts.dispatcher import IncidentAlert


class AlertDeduplicator:
    """Suppresses duplicate alert notifications within configurable cooldown windows."""

    def __init__(self, cooldown_seconds: int = 300):
        self.cooldown_seconds = cooldown_seconds
        self._last_alert_times: Dict[str, float] = {}

    def compute_fingerprint(self, alert: IncidentAlert) -> str:
        key = f"{alert.severity}:{alert.pipeline_id}:{alert.dataset_name}:{alert.title}"
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    def should_suppress(self, alert: IncidentAlert) -> bool:
        fp = self.compute_fingerprint(alert)
        now = time.time()
        last_sent = self._last_alert_times.get(fp, 0.0)

        if now - last_sent < self.cooldown_seconds:
            return True

        self._last_alert_times[fp] = now
        return False
