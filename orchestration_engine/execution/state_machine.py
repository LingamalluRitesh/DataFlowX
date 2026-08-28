"""
DataFlowX Pipeline Execution Lifecycle State Machine
Enforces state transitions across CREATED -> QUEUED -> RUNNING -> SUCCESS / FAILED / UPSTREAM_FAILED / RETRYING / CANCELLED with audit transitions.
"""

from typing import List, Optional, Set
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class StateTransition(BaseModel):
    from_state: str
    to_state: str
    timestamp_unix: float
    reason: Optional[str] = None


class PipelineStateMachine:
    """Finite state machine governing task and pipeline lifecycles."""

    VALID_TRANSITIONS: Dict[str, Set[str]] = {
        "CREATED": {"QUEUED", "CANCELLED"},
        "QUEUED": {"RUNNING", "CANCELLED"},
        "RUNNING": {"SUCCESS", "FAILED", "RETRYING", "CANCELLED"},
        "RETRYING": {"QUEUED", "FAILED", "CANCELLED"},
        "SUCCESS": set(),
        "FAILED": {"RETRYING"},
        "UPSTREAM_FAILED": set(),
        "CANCELLED": set(),
    }

    def __init__(self, run_id: str, initial_state: str = "CREATED"):
        self.run_id = run_id
        self.current_state = initial_state
        self.history: List[StateTransition] = []

    def transition_to(self, new_state: str, reason: Optional[str] = None) -> bool:
        import time
        allowed = self.VALID_TRANSITIONS.get(self.current_state, set())
        if new_state not in allowed:
            logger.error(f"Illegal state transition from '{self.current_state}' to '{new_state}' for run '{self.run_id}'")
            return False

        t = StateTransition(from_state=self.current_state, to_state=new_state, timestamp_unix=time.time(), reason=reason)
        self.history.append(t)
        self.current_state = new_state
        logger.info(f"Run '{self.run_id}' transitioned to state: {new_state} ({reason or 'no reason'})")
        return True
