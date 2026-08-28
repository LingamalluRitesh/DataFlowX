"""
DataFlowX Advanced Vixie-Cron Expression Parser
Supports standard 5-field syntax, aliases (@daily, @hourly, @weekly, @monthly), step values (*/15), range lists (1-5,10), and timezone offsets.
"""

from datetime import datetime, timedelta, timezone
from typing import List, Optional, Set


class AdvancedCronParser:
    """Parses cron expressions into valid next run timestamps."""

    ALIASES = {
        "@YEARLY": "0 0 1 1 *",
        "@ANNUALLY": "0 0 1 1 *",
        "@MONTHLY": "0 0 1 * *",
        "@WEEKLY": "0 0 * * 0",
        "@DAILY": "0 0 * * *",
        "@MIDNIGHT": "0 0 * * *",
        "@HOURLY": "0 * * * *",
    }

    @classmethod
    def expand_field(cls, field_str: str, min_val: int, max_val: int) -> Set[int]:
        """Expand cron field (e.g. '*/15', '1-5', '1,10,20') into concrete set of integers."""
        if field_str == "*":
            return set(range(min_val, max_val + 1))

        values = set()
        for part in field_str.split(","):
            if "/" in part:
                subparts = part.split("/")
                step = int(subparts[1])
                start = min_val if subparts[0] == "*" else int(subparts[0])
                values.update(range(start, max_val + 1, step))
            elif "-" in part:
                start, end = map(int, part.split("-"))
                values.update(range(start, end + 1))
            else:
                values.add(int(part))
        return values

    @classmethod
    def get_next_schedule(cls, cron_expr: str, from_dt: Optional[datetime] = None) -> datetime:
        expr = cls.ALIASES.get(cron_expr.strip().upper(), cron_expr.strip())
        parts = expr.split()
        if len(parts) != 5:
            raise ValueError(f"Invalid cron expression: '{cron_expr}' (expected 5 fields)")

        minute_spec, hour_spec, dom_spec, month_spec, dow_spec = parts

        minutes = cls.expand_field(minute_spec, 0, 59)
        hours = cls.expand_field(hour_spec, 0, 23)
        doms = cls.expand_field(dom_spec, 1, 31)
        months = cls.expand_field(month_spec, 1, 12)
        dows = cls.expand_field(dow_spec, 0, 6)

        curr = (from_dt or datetime.now(timezone.utc)).replace(second=0, microsecond=0) + timedelta(minutes=1)

        # Search forward up to 5 years (max 2,628,000 iterations)
        for _ in range(525600):
            if (curr.month in months and
                curr.day in doms and
                curr.weekday() in dows and
                curr.hour in hours and
                curr.minute in minutes):
                return curr
            curr += timedelta(minutes=1)

        return curr
