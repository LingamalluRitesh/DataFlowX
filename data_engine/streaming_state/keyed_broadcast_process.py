"""
DataFlowX Broadcast State Pattern Stream Processor
Enables real-time dynamic rule and configuration broadcasting to parallel keyed data streams without pipeline restarts.
"""

from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field


class BroadcastRule(BaseModel):
    rule_id: str
    target_metric: str
    operator: str  # >, <, ==, !=
    threshold: float
    action: str = "ALERT"


class KeyedBroadcastProcessor:
    """Processes keyed data elements against broadcasted rules."""

    def __init__(self):
        self.broadcast_rules: Dict[str, BroadcastRule] = {}
        self.keyed_counters: Dict[str, Dict[str, float]] = {}

    def update_rule(self, rule: BroadcastRule) -> None:
        self.broadcast_rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> None:
        self.broadcast_rules.pop(rule_id, None)

    def process_element(self, key: str, metric_name: str, value: float) -> List[Dict[str, Any]]:
        """Evaluates incoming keyed element against broadcast state."""
        if key not in self.keyed_counters:
            self.keyed_counters[key] = {}
        self.keyed_counters[key][metric_name] = value

        alerts = []
        for r in self.broadcast_rules.values():
            if r.target_metric == metric_name:
                matched = False
                if r.operator == ">" and value > r.threshold:
                    matched = True
                elif r.operator == "<" and value < r.threshold:
                    matched = True
                elif r.operator == "==" and value == r.threshold:
                    matched = True

                if matched:
                    alerts.append({
                        "key": key,
                        "rule_id": r.rule_id,
                        "metric": metric_name,
                        "current_value": value,
                        "threshold": r.threshold,
                        "action": r.action
                    })

        return alerts
