"""
DataFlowX Streaming Temporal Interval Join
Performs stateful interval joins between two unbounded streaming sources within lower and upper time bounds [event_a.ts - lower_bound, event_a.ts + upper_bound].
"""

from typing import Any, Dict, List, Optional
import pandas as pd


class StreamingIntervalJoiner:
    """Joins two real-time event streams within temporal bounds."""

    @classmethod
    def interval_join(
        cls,
        left_events: List[Dict[str, Any]],
        right_events: List[Dict[str, Any]],
        join_key: str,
        time_key: str,
        lower_bound_sec: float = 60.0,
        upper_bound_sec: float = 60.0
    ) -> List[Dict[str, Any]]:
        joined = []
        for l in left_events:
            l_key = l.get(join_key)
            l_ts = l.get(time_key, 0.0)
            for r in right_events:
                if r.get(join_key) == l_key:
                    r_ts = r.get(time_key, 0.0)
                    if (l_ts - lower_bound_sec) <= r_ts <= (l_ts + upper_bound_sec):
                        joined.append({"left": l, "right": r, "joined_ts": max(l_ts, r_ts)})
        return joined
