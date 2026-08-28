"""
DataFlowX Declarative Complex Event Processing Rule DSL Parser
Compiles human-readable pattern strings (e.g., `PATTERN (FailedLogin -> FailedLogin -> AccountLocked) WITHIN 5m`) into executable pattern matchers.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field
from data_engine.cep.pattern_matcher import CEPPatternMatcher


class CEPRuleDefinition(BaseModel):
    rule_name: str
    event_sequence: List[str]
    within_seconds: float = 300.0


class CEPRuleParser:
    """Parses declarative CEP rules."""

    @classmethod
    def parse_rule(cls, rule_name: str, sequence: List[str], window_seconds: float = 300.0) -> CEPPatternMatcher:
        return CEPPatternMatcher(pattern_name=rule_name, max_interval_seconds=window_seconds)
