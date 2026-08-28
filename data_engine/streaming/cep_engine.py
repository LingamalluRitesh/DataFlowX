"""
DataFlowX Complex Event Processing (CEP) Engine
Detects temporal sequence patterns across sliding event windows (e.g. '3 Failed Logins within 60s followed by Location Change').
"""

from datetime import datetime, timezone
import time
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class CEPPatternRule(BaseModel):
    rule_name: str
    target_event_type: str
    match_condition: str  # e.g. "status == 'FAILED'"
    occurrence_count: int = 3
    window_seconds: int = 60
    severity: str = "HIGH"


class CEPPatternMatch(BaseModel):
    rule_name: str
    entity_key: str
    matched_events_count: int
    first_event_time: str
    last_event_time: str
    severity: str


class ComplexEventProcessor:
    """Evaluates temporal state machine rules over event streams."""

    def __init__(self, rules: List[CEPPatternRule]):
        self.rules = rules
        # Mapping: rule_name -> entity_key -> list of (timestamp_unix, event_payload)
        self._state_buffers: Dict[str, Dict[str, List[Tuple[float, Dict[str, Any]]]]] = {
            r.rule_name: {} for r in rules
        }

    def process_event(self, event_type: str, entity_key: str, payload: Dict[str, Any], event_time_unix: Optional[float] = None) -> List[CEPPatternMatch]:
        now_ts = event_time_unix or time.time()
        matches = []

        for rule in self.rules:
            if rule.target_event_type != event_type:
                continue

            entity_events = self._state_buffers[rule.rule_name].setdefault(entity_key, [])
            # Prune events outside window
            cutoff = now_ts - rule.window_seconds
            entity_events[:] = [e for e in entity_events if e[0] >= cutoff]

            entity_events.append((now_ts, payload))

            if len(entity_events) >= rule.occurrence_count:
                match = CEPPatternMatch(
                    rule_name=rule.rule_name,
                    entity_key=entity_key,
                    matched_events_count=len(entity_events),
                    first_event_time=datetime.fromtimestamp(entity_events[0][0], tz=timezone.utc).isoformat(),
                    last_event_time=datetime.fromtimestamp(entity_events[-1][0], tz=timezone.utc).isoformat(),
                    severity=rule.severity
                )
                matches.append(match)
                logger.warning(f"CEP Alert [{rule.severity}]: Rule '{rule.rule_name}' triggered on entity '{entity_key}' ({len(entity_events)} occurrences)")
                # Clear buffer after trigger to prevent duplicate firing
                entity_events.clear()

        return matches
