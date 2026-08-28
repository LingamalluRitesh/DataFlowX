"""
DataFlowX Complex Event Processing (CEP) State Machine Pattern Matcher
Executes Non-Deterministic Finite Automata (NFA) state machines over event streams to detect multi-event sequences (e.g., A followed by B within T seconds).
"""

from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field


class CEPPatternMatch(BaseModel):
    pattern_name: str
    matched_events: List[Dict[str, Any]] = Field(default_factory=list)
    start_time_unix: float
    end_time_unix: float


class CEPPatternMatcher:
    """NFA-based CEP sequence matcher."""

    def __init__(self, pattern_name: str, max_interval_seconds: float = 300.0):
        self.pattern_name = pattern_name
        self.max_interval_seconds = max_interval_seconds

    def match_sequence(
        self,
        events: List[Dict[str, Any]],
        predicates: List[Callable[[Dict[str, Any]], bool]]
    ) -> List[CEPPatternMatch]:
        matches = []
        if len(predicates) < 2:
            return matches

        for i, first_evt in enumerate(events):
            if predicates[0](first_evt):
                t0 = first_evt.get("timestamp_unix", 0.0)
                # Look ahead for second predicate
                for second_evt in events[i + 1:]:
                    t1 = second_evt.get("timestamp_unix", 0.0)
                    if (t1 - t0) > self.max_interval_seconds:
                        break  # Interval exceeded
                    if predicates[1](second_evt):
                        matches.append(CEPPatternMatch(
                            pattern_name=self.pattern_name,
                            matched_events=[first_evt, second_evt],
                            start_time_unix=t0,
                            end_time_unix=t1
                        ))
        return matches
