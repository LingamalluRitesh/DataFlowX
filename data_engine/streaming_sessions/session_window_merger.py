"""
DataFlowX Streaming Session Window Merger
Dynamically merges overlapping active user session intervals based on inactivity gap thresholds (e.g. 30 minutes).
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class UserSessionWindow(BaseModel):
    session_id: str
    user_key: str
    start_timestamp_ms: int
    end_timestamp_ms: int
    event_count: int = 1


class StreamingSessionWindowMerger:
    """Manages session merging per user key."""

    def __init__(self, inactivity_gap_ms: int = 1800000):  # 30 mins
        self.inactivity_gap_ms = inactivity_gap_ms
        # user_key -> list of UserSessionWindow
        self.user_sessions: Dict[str, List[UserSessionWindow]] = {}

    def process_event(self, user_key: str, event_time_ms: int) -> UserSessionWindow:
        if user_key not in self.user_sessions:
            self.user_sessions[user_key] = []

        sessions = self.user_sessions[user_key]

        # Check if can merge into latest session
        if sessions and (event_time_ms - sessions[-1].end_timestamp_ms <= self.inactivity_gap_ms):
            last_sess = sessions[-1]
            last_sess.end_timestamp_ms = max(last_sess.end_timestamp_ms, event_time_ms)
            last_sess.event_count += 1
            return last_sess
        else:
            # Create new session
            new_sess = UserSessionWindow(
                session_id=f"sess_{user_key}_{event_time_ms}",
                user_key=user_key,
                start_timestamp_ms=event_time_ms,
                end_timestamp_ms=event_time_ms,
                event_count=1
            )
            sessions.append(new_sess)
            return new_sess
