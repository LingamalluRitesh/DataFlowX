"""
DataFlowX Text Processing & NLP Parsing Operators
Provides regular expression entity extractions, email domain parsing, URL query parsing, sentiment scoring, and tokenization.
"""

import re
from typing import Any, Dict, List, Optional, Tuple, Union
import urllib.parse
import pandas as pd

from backend.core.logging import get_logger
from data_engine.transformation.operators import BaseOperator

logger = get_logger(__name__)


class RegexEntityExtractOperator(BaseOperator):
    """Extracts regex capture groups from unstructured text into designated columns."""

    def __init__(self, target_column: str, pattern: str, output_columns: List[str]):
        self.target_column = target_column
        self.pattern = re.compile(pattern)
        self.output_columns = output_columns

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.target_column not in df.columns:
            return df
        df = df.copy()

        extracted = df[self.target_column].astype(str).str.extract(self.pattern)
        if not extracted.empty:
            for idx, col in enumerate(self.output_columns):
                if idx < extracted.shape[1]:
                    df[col] = extracted[idx]
        return df


class EmailDomainExtractOperator(BaseOperator):
    """Extracts user handle, domain name, and top-level domain (TLD) from email addresses."""

    def __init__(self, email_column: str, output_domain_col: str = "email_domain", output_user_col: Optional[str] = None):
        self.email_column = email_column
        self.output_domain_col = output_domain_col
        self.output_user_col = output_user_col

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.email_column not in df.columns:
            return df
        df = df.copy()

        def parse_email(val: Any) -> Tuple[Optional[str], Optional[str]]:
            if not val or not isinstance(val, str) or "@" not in val:
                return None, None
            parts = val.strip().split("@", 1)
            return parts[0], parts[1].lower()

        parsed = df[self.email_column].apply(parse_email)
        if self.output_user_col:
            df[self.output_user_col] = parsed.apply(lambda p: p[0])
        df[self.output_domain_col] = parsed.apply(lambda p: p[1])
        return df


class URLParserOperator(BaseOperator):
    """Deconstructs web URLs into scheme, netloc (hostname), path, query params, and UTM tags."""

    def __init__(self, url_column: str, prefix: str = "url"):
        self.url_column = url_column
        self.prefix = prefix

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.url_column not in df.columns:
            return df
        df = df.copy()

        def parse_url(val: Any) -> Dict[str, Any]:
            if not val or not isinstance(val, str):
                return {}
            try:
                parsed = urllib.parse.urlparse(val)
                query_dict = urllib.parse.parse_qs(parsed.query)
                return {
                    f"{self.prefix}_scheme": parsed.scheme,
                    f"{self.prefix}_host": parsed.netloc,
                    f"{self.prefix}_path": parsed.path,
                    f"{self.prefix}_utm_source": query_dict.get("utm_source", [None])[0],
                    f"{self.prefix}_utm_campaign": query_dict.get("utm_campaign", [None])[0],
                    f"{self.prefix}_utm_medium": query_dict.get("utm_medium", [None])[0],
                }
            except Exception:
                return {}

        url_features = df[self.url_column].apply(parse_url).tolist()
        df_feat = pd.DataFrame(url_features, index=df.index)
        return pd.concat([df, df_feat], axis=1)


class RuleBasedSentimentScorer(BaseOperator):
    """High-speed vectorized lexicon sentiment analyzer (Positive, Neutral, Negative)."""

    POSITIVE_WORDS = {
        "good", "great", "excellent", "amazing", "love", "awesome", "fast", "reliable",
        "happy", "best", "perfect", "fantastic", "helpful", "recommend", "superior"
    }
    NEGATIVE_WORDS = {
        "bad", "terrible", "horrible", "hate", "slow", "broken", "fail", "bug", "crash",
        "awful", "worst", "poor", "useless", "disappointed", "error", "unreliable"
    }

    def __init__(self, text_column: str, output_col: str = "sentiment_score", output_label_col: str = "sentiment_label"):
        self.text_column = text_column
        self.output_col = output_col
        self.output_label_col = output_label_col

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.text_column not in df.columns:
            return df
        df = df.copy()

        def score_text(val: Any) -> Tuple[float, str]:
            if not val or not isinstance(val, str):
                return 0.0, "NEUTRAL"
            words = set(re.findall(r"\b\w+\b", val.lower()))
            pos_count = len(words.intersection(self.POSITIVE_WORDS))
            neg_count = len(words.intersection(self.NEGATIVE_WORDS))
            total = pos_count + neg_count
            if total == 0:
                return 0.0, "NEUTRAL"
            score = round((pos_count - neg_count) / total, 2)
            if score > 0.15:
                label = "POSITIVE"
            elif score < -0.15:
                label = "NEGATIVE"
            else:
                label = "NEUTRAL"
            return score, label

        scored = df[self.text_column].apply(score_text)
        df[self.output_col] = scored.apply(lambda s: s[0])
        df[self.output_label_col] = scored.apply(lambda s: s[1])
        return df
