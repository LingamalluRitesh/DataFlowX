"""
DataFlowX Non-Deterministic Finite Automaton (NFA) Streaming Pattern Matcher
Tracks complex event processing sequences (e.g., A -> B within window W while NOT C).
"""

from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field


class CEPEvent(BaseModel):
    event_type: str
    timestamp_ms: int
    payload: Dict[str, Any] = Field(default_factory=dict)


class NFAState(BaseModel):
    state_name: str
    is_start: bool = False
    is_terminal: bool = False


class NFATransition:
    def __init__(self, from_state: str, to_state: str, condition: Callable[[CEPEvent, Dict[str, Any]], bool]):
        self.from_state = from_state
        self.to_state = to_state
        self.condition = condition


class NFAEngine:
    """NFA Pattern Matching Engine."""

    def __init__(self, window_ms: int = 60000):
        self.window_ms = window_ms
        self.states: Dict[str, NFAState] = {}
        self.transitions: List[NFATransition] = []
        # Active computation branches: list of (current_state, matched_events, start_timestamp)
        self.active_computations: List[tuple[str, List[CEPEvent], int]] = []

    def add_state(self, state: NFAState) -> None:
        self.states[state.state_name] = state

    def add_transition(self, from_state: str, to_state: str, condition: Callable[[CEPEvent, Dict[str, Any]], bool]) -> None:
        self.transitions.append(NFATransition(from_state, to_state, condition))

    def process_event(self, event: CEPEvent) -> List[List[CEPEvent]]:
        """Consumes an event and returns any newly completed pattern matches."""
        completed_matches: List[List[CEPEvent]] = []
        next_computations = []

        # 1. Spawn new computation from start states
        for s_name, state in self.states.items():
            if state.is_start:
                for trans in self.transitions:
                    if trans.from_state == s_name and trans.condition(event, {}):
                        if self.states[trans.to_state].is_terminal:
                            completed_matches.append([event])
                        else:
                            next_computations.append((trans.to_state, [event], event.timestamp_ms))

        # 2. Advance existing computations
        for curr_state, history, start_ts in self.active_computations:
            # Check window expiry
            if event.timestamp_ms - start_ts > self.window_ms:
                continue

            ctx = {e.event_type: e.payload for e in history}
            matched_any = False
            for trans in self.transitions:
                if trans.from_state == curr_state and trans.condition(event, ctx):
                    new_history = list(history) + [event]
                    if self.states[trans.to_state].is_terminal:
                        completed_matches.append(new_history)
                    else:
                        next_computations.append((trans.to_state, new_history, start_ts))
                    matched_any = True

            # Also maintain computation if it allows skipped events (loose contiguity)
            if not matched_any:
                next_computations.append((curr_state, history, start_ts))

        self.active_computations = next_computations
        return completed_matches
