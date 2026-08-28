"""
DataFlowX Streaming Session State Store with Checkpointed State
Maintains per-session user window state, accumulated aggregates, and timer states for Stateful streaming stream processors.
"""

from collections import OrderedDict
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class UserSessionState(BaseModel):
    session_id: str
    user_id: str
    session_start_unix: float
    last_event_unix: float
    event_count: int = 0
    accumulated_metrics: Dict[str, float] = Field(default_factory=dict)
    is_expired: bool = False


class StreamingSessionStateStore:
    """Manages active streaming user sessions."""

    def __init__(self, inactivity_timeout_seconds: float = 1800.0, max_active_sessions: int = 50000):
        self.inactivity_timeout_seconds = inactivity_timeout_seconds
        self.max_active_sessions = max_active_sessions
        self._sessions: OrderedDict[str, UserSessionState] = OrderedDict()

    def record_session_event(self, session_id: str, user_id: str, metric_delta: float = 1.0) -> UserSessionState:
        now = time.time()
        if session_id in self._sessions:
            sess = self._sessions[session_id]
            sess.last_event_unix = now
            sess.event_count += 1
            sess.accumulated_metrics["total_value"] = sess.accumulated_metrics.get("total_value", 0.0) + metric_delta
            self._sessions.move_to_end(session_id)
            return sess
        else:
            sess = UserSessionState(
                session_id=session_id,
                user_id=user_id,
                session_start_unix=now,
                last_event_unix=now,
                event_count=1,
                accumulated_metrics={"total_value": metric_delta}
            )
            self._sessions[session_id] = sess
            if len(self._sessions) > self.max_active_sessions:
                self._sessions.popitem(last=False)
            return sess

    def evict_expired_sessions(self) -> List[UserSessionState]:
        now = time.time()
        expired = []
        for sess_id, sess in list(self._sessions.items()):
            if now - sess.last_event_unix > self.inactivity_timeout_seconds:
                sess.is_expired = True
                expired.append(sess)
                del self._sessions[sess_id]
        return expired
