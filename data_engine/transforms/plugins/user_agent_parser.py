"""
DataFlowX User-Agent HTTP Header Parsing Plugin
Classifies browser family (Chrome, Safari, Firefox, Edge), OS family (Windows, macOS, Linux, iOS, Android), device type (Desktop, Mobile, Tablet, Bot), and crawler flags.
"""

import re
from typing import Any, Dict, Optional
import pandas as pd


class UserAgentParserPlugin:
    """Classifies user agent strings."""

    @classmethod
    def parse_user_agent(cls, ua_str: str) -> Dict[str, str]:
        if not ua_str or not isinstance(ua_str, str):
            return {"browser": "Unknown", "os": "Unknown", "device_type": "Unknown", "is_bot": "False"}

        ua = ua_str.lower()
        is_bot = "bot" in ua or "crawler" in ua or "spider" in ua

        # Device Type
        if is_bot:
            device = "Bot"
        elif "tablet" in ua or "ipad" in ua:
            device = "Tablet"
        elif "mobile" in ua or "iphone" in ua or "android" in ua:
            device = "Mobile"
        else:
            device = "Desktop"

        # OS
        if "windows" in ua:
            os_name = "Windows"
        elif "macintosh" in ua or "mac os" in ua:
            os_name = "macOS"
        elif "android" in ua:
            os_name = "Android"
        elif "iphone" in ua or "ipad" in ua:
            os_name = "iOS"
        elif "linux" in ua:
            os_name = "Linux"
        else:
            os_name = "Other"

        # Browser
        if "edg" in ua:
            browser = "Edge"
        elif "chrome" in ua and "safari" in ua:
            browser = "Chrome"
        elif "safari" in ua and "chrome" not in ua:
            browser = "Safari"
        elif "firefox" in ua:
            browser = "Firefox"
        else:
            browser = "Other"

        return {
            "browser": browser,
            "os": os_name,
            "device_type": device,
            "is_bot": str(is_bot)
        }

    @classmethod
    def apply_ua_enrichment(cls, df: pd.DataFrame, ua_col: str) -> pd.DataFrame:
        if df.empty or ua_col not in df.columns:
            return df
        df = df.copy()
        parsed_records = df[ua_col].apply(cls.parse_user_agent)
        parsed_df = pd.DataFrame(list(parsed_records), index=df.index)
        return pd.concat([df, parsed_df], axis=1)
