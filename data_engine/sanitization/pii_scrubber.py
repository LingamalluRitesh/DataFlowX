"""
DataFlowX Regex & Pattern PII Data Scrubber
Scans column string records and replaces Social Security Numbers (SSNs), Credit Card PANs, Emails, and Phone Numbers with compliant redaction masks.
"""

import re
from typing import Any, Dict


class PIIScrubber:
    """Detects and scrubs PII from string records."""

    EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    SSN_REGEX = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
    CC_REGEX = re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b")
    PHONE_REGEX = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")

    @classmethod
    def scrub_text(cls, text: str) -> str:
        s = text
        s = cls.EMAIL_REGEX.sub("[REDACTED_EMAIL]", s)
        s = cls.SSN_REGEX.sub("[REDACTED_SSN]", s)
        s = cls.CC_REGEX.sub("[REDACTED_CC]", s)
        s = cls.PHONE_REGEX.sub("[REDACTED_PHONE]", s)
        return s

    @classmethod
    def scrub_record(cls, record: Dict[str, Any]) -> Dict[str, Any]:
        return {k: cls.scrub_text(str(v)) if isinstance(v, str) else v for k, v in record.items()}
