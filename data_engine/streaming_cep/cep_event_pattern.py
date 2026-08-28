"""
DataFlowX Complex Event Processing (CEP) Pattern Compiler
Compiles declarative sequence rules (e.g. Fraud Detection: LoginFailed x 3 within 5m followed by PasswordReset) into NFAs.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field
from data_engine.streaming_cep.nfa_engine import CEPEvent, NFAEngine, NFAState


class CEPPatternDefinition(BaseModel):
    pattern_name: str
    event_types: List[str]
    time_window_seconds: int = 300
    alert_severity: str = "HIGH"


class CEPPatternCompiler:
    """Compiles declarative patterns into NFA execution engines."""

    @classmethod
    def compile_sequence(cls, pattern: CEPPatternDefinition) -> NFAEngine:
        engine = NFAEngine(window_ms=pattern.time_window_seconds * 1000)

        # Create states
        start_state = NFAState(state_name="S0", is_start=True)
        engine.add_state(start_state)

        for i, ev_type in enumerate(pattern.event_types):
            next_state_name = f"S{i+1}"
            is_term = (i == len(pattern.event_types) - 1)
            state = NFAState(state_name=next_state_name, is_terminal=is_term)
            engine.add_state(state)

            prev_state_name = f"S{i}"
            expected_type = ev_type

            # Add transition condition checking event_type
            def make_cond(target_type):
                return lambda ev, ctx: ev.event_type == target_type

            engine.add_transition(prev_state_name, next_state_name, make_cond(expected_type))

        return engine
