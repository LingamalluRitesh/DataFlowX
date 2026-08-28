"""
DataFlowX Cron & Schedule Evaluator
Evaluates standard 5-field cron expressions and intervals with timezone support.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from croniter import croniter
from backend.core.logging import get_logger

logger = get_logger(__name__)


class ScheduleEvaluator:
    """Computes next execution timestamps for pipeline schedules."""

    @staticmethod
    def is_due(
        next_run_at: Optional[datetime],
        current_time: Optional[datetime] = None
    ) -> bool:
        """Check if schedule is currently due for execution."""
        if not next_run_at:
            return True
        now = current_time or datetime.now(timezone.utc)
        return now >= next_run_at

    @staticmethod
    def get_next_run(
        cron_expression: Optional[str] = None,
        interval_seconds: Optional[int] = None,
        base_time: Optional[datetime] = None
    ) -> datetime:
        """Calculate next scheduled datetime from cron expression or interval."""
        now = base_time or datetime.now(timezone.utc)

        if cron_expression:
            try:
                iter_obj = croniter(cron_expression, now)
                next_ts = iter_obj.get_next(datetime)
                if next_ts.tzinfo is None:
                    next_ts = next_ts.replace(tzinfo=timezone.utc)
                return next_ts
            except Exception as exc:
                logger.error(f"Invalid cron expression '{cron_expression}': {exc}")
                return now + timedelta(hours=1)

        elif interval_seconds and interval_seconds > 0:
            return now + timedelta(seconds=interval_seconds)

        return now + timedelta(days=1)
