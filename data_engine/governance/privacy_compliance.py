"""
DataFlowX GDPR / CCPA Privacy & PII Classification Engine
Scans column schemas and record samples to automatically classify sensitive PII (Personally Identifiable Information) and generate compliance reports.
"""

import re
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import pandas as pd
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class PIIFieldMatch(BaseModel):
    column_name: str
    pii_type: str  # EMAIL, PHONE_NUMBER, CREDIT_CARD, SSN, IP_ADDRESS, PERSON_NAME, POSTAL_CODE
    confidence: float  # [0.0, 1.0]
    matched_by: str  # HEADER_NAME, REGEX_SAMPLE
    sample_match_count: int


class PrivacyScanReport(BaseModel):
    dataset_name: str
    total_columns_scanned: int
    pii_columns_detected: List[PIIFieldMatch] = Field(default_factory=list)
    gdpr_sensitivity_level: str = "LOW"  # LOW, MEDIUM, HIGH, RESTRICTED
    scanned_at: str = Field(default_factory=lambda: pd.Timestamp.now(tz="UTC").isoformat())


class PrivacyComplianceScanner:
    """Automated PII scanner utilizing column naming heuristics and regex sample matching."""

    HEADER_PATTERNS = {
        "EMAIL": re.compile(r"email|e_mail|mail_address", re.IGNORECASE),
        "PHONE_NUMBER": re.compile(r"phone|mobile|cell|telephone|fax", re.IGNORECASE),
        "CREDIT_CARD": re.compile(r"card_num|credit_card|pan|cc_num", re.IGNORECASE),
        "SSN": re.compile(r"ssn|social_sec|national_id", re.IGNORECASE),
        "PERSON_NAME": re.compile(r"first_name|last_name|full_name|customer_name|surname", re.IGNORECASE),
        "IP_ADDRESS": re.compile(r"ip_address|client_ip|remote_addr", re.IGNORECASE),
        "POSTAL_CODE": re.compile(r"zip_code|postal_code|postcode", re.IGNORECASE),
    }

    VALUE_PATTERNS = {
        "EMAIL": re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
        "PHONE_NUMBER": re.compile(r"^\+?[0-9\s\-()]{7,20}$"),
        "CREDIT_CARD": re.compile(r"^[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}$"),
        "IP_ADDRESS": re.compile(r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"),
    }

    @classmethod
    def scan_dataframe(cls, df: pd.DataFrame, dataset_name: str = "dataset") -> PrivacyScanReport:
        matches = []
        if df.empty:
            return PrivacyScanReport(dataset_name=dataset_name, total_columns_scanned=0)

        for col in df.columns:
            col_str = str(col)
            # 1. Header Name Match
            for pii_type, pattern in cls.HEADER_PATTERNS.items():
                if pattern.search(col_str):
                    matches.append(PIIFieldMatch(
                        column_name=col_str,
                        pii_type=pii_type,
                        confidence=0.85,
                        matched_by="HEADER_NAME",
                        sample_match_count=0
                    ))
                    break

            # 2. Sample Value Match
            sample_slice = df[col].dropna().astype(str).head(100)
            if not sample_slice.empty:
                for pii_type, pattern in cls.VALUE_PATTERNS.items():
                    match_count = sum(1 for v in sample_slice if pattern.match(v))
                    if match_count >= 5:
                        confidence = round(match_count / len(sample_slice), 2)
                        # Check if already added by header
                        existing = next((m for m in matches if m.column_name == col_str), None)
                        if not existing:
                            matches.append(PIIFieldMatch(
                                column_name=col_str,
                                pii_type=pii_type,
                                confidence=confidence,
                                matched_by="REGEX_SAMPLE",
                                sample_match_count=match_count
                            ))
                        else:
                            existing.confidence = max(existing.confidence, confidence)
                            existing.sample_match_count = match_count

        sensitivity = "LOW"
        pii_types = {m.pii_type for m in matches}
        if "CREDIT_CARD" in pii_types or "SSN" in pii_types:
            sensitivity = "RESTRICTED"
        elif "EMAIL" in pii_types or "PHONE_NUMBER" in pii_types or "PERSON_NAME" in pii_types:
            sensitivity = "HIGH"
        elif matches:
            sensitivity = "MEDIUM"

        return PrivacyScanReport(
            dataset_name=dataset_name,
            total_columns_scanned=len(df.columns),
            pii_columns_detected=matches,
            gdpr_sensitivity_level=sensitivity
        )
