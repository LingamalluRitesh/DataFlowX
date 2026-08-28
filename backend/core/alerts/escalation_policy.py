"""
DataFlowX Escalation Policy & On-Call Rotation Engine
Defines tiered escalation steps (Tier 1 -> Tier 2 -> On-Call Lead) with timeout timeouts when incidents remain unacknowledged.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EscalationTarget(BaseModel):
    target_type: str  # USER, SCHEDULE, SLACK_CHANNEL, PAGERDUTY_SERVICE
    target_id: str


class EscalationRule(BaseModel):
    step_number: int
    delay_minutes: int
    targets: List[EscalationTarget] = Field(default_factory=list)


class EscalationPolicy(BaseModel):
    id: str
    name: str
    description: str
    repeat_count: int = 2
    rules: List[EscalationRule] = Field(default_factory=list)
