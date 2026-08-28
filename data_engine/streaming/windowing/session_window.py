"""
DataFlowX Streaming Session Window State Merger
Dynamically groups user event streams into activity sessions, splitting or merging sessions when inactivity gaps exceed the configured session timeout threshold.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class StreamSession(BaseModel):
    session_id: str
    entity_id: str
    start_time_unix: float
    end_time_unix: float
    event_count: int = 0
    total_value: float = 0.0


class SessionWindowManager:
    """Maintains active user streaming sessions."""

    def __init__(self, inactivity_gap_seconds: int = 1800):  # 30 min default
        self.inactivity_gap_seconds = inactivity_gap_seconds
        # entity_id -> StreamSession
        self._active_sessions: Dict[str, StreamSession] = {}

    def process_event(self, entity_id: str, event_time_unix: float, value: float = 0.0) -> Optional[StreamSession]:
        """
        Process event. If previous session expired, closes and returns old session, starting a new one.
        """
        closed_session = None
        curr = self._active_sessions.get(entity_id)

        if curr:
            if event_time_unix - curr.end_time_unix > self.inactivity_gap_seconds:
                # Inactivity gap exceeded -> close current session
                closed_session = curr
                # Start new session
                self._active_sessions[entity_id] = StreamSession(
                    session_id=f"sess_{entity_id}_{int(event_time_unix)}",
                    entity_id=entity_id,
                    start_time_unix=event_time_unix,
                    end_time_unix=event_time_unix,
                    event_count=1,
                    total_value=value
                )
            else:
                # Extend current session
                curr.end_time_unix = max(curr.end_time_unix, event_time_unix)
                curr.event_count += 1
                curr.total_value += value
        else:
            self._active_sessions[entity_id] = StreamSession(
                session_id=f"sess_{entity_id}_{int(event_time_unix)}",
                entity_id=entity_id,
                start_time_unix=event_time_unix,
                end_time_unix=event_time_unix,
                event_count=1,
                total_value=value
            )

        return closed_session
