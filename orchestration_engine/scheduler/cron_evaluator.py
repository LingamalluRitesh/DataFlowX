"""
DataFlowX Cron Expression Evaluator & Next Execution Calculation
Parses 5-field cron strings and determines precise next scheduled UTC run timestamps.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
import croniter


class CronEvaluator:
    """Evaluates standard cron expressions (e.g. '0 0 * * *', '*/15 * * * *')."""

    @staticmethod
    def get_next_run(cron_expression: str, base_time: Optional[datetime] = None) -> datetime:
        base = base_time or datetime.now(timezone.utc)
        iter_obj = croniter.croniter(cron_expression, base)
        return iter_obj.get_next(datetime)

    @staticmethod
    def get_next_n_runs(cron_expression: str, count: int = 5, base_time: Optional[datetime] = None) -> List[datetime]:
        base = base_time or datetime.now(timezone.utc)
        iter_obj = croniter.croniter(cron_expression, base)
        runs = []
        for _ in range(count):
            runs.append(iter_obj.get_next(datetime))
        return runs

    @staticmethod
    def is_valid_cron(cron_expression: str) -> bool:
        return croniter.croniter.is_valid(cron_expression)


ScheduleEvaluator = CronEvaluator
