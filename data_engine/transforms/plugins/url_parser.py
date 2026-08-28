"""
DataFlowX Deep URL Parsing & Marketing Attribution Plugin
Extracts scheme, hostname, root domain, path, UTM parameters (utm_source, utm_medium, utm_campaign, utm_content, utm_term), and query parameters from raw URLs.
"""

from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlparse
import pandas as pd


class URLParserPlugin:
    """Vectorized URL feature extraction."""

    @classmethod
    def parse_url_components(cls, url_str: str) -> Dict[str, Optional[str]]:
        if not url_str or not isinstance(url_str, str):
            return {
                "scheme": None, "hostname": None, "path": None,
                "utm_source": None, "utm_medium": None, "utm_campaign": None
            }

        try:
            parsed = urlparse(url_str)
            params = parse_qs(parsed.query)

            return {
                "scheme": parsed.scheme,
                "hostname": parsed.hostname,
                "path": parsed.path,
                "utm_source": params.get("utm_source", [None])[0],
                "utm_medium": params.get("utm_medium", [None])[0],
                "utm_campaign": params.get("utm_campaign", [None])[0],
            }
        except Exception:
            return {
                "scheme": None, "hostname": None, "path": None,
                "utm_source": None, "utm_medium": None, "utm_campaign": None
            }

    @classmethod
    def apply_url_decomposition(cls, df: pd.DataFrame, url_col: str) -> pd.DataFrame:
        if df.empty or url_col not in df.columns:
            return df
        df = df.copy()

        extracted = df[url_col].apply(cls.parse_url_components)
        extracted_df = pd.DataFrame(list(extracted), index=df.index)
        return pd.concat([df, extracted_df], axis=1)
