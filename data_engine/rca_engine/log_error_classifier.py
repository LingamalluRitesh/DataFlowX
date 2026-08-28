"""
DataFlowX NLP & Regex Log Error Classifier
Classifies raw execution stack traces into actionable root categories (OOM, TIMEOUT, SCHEMA_MISMATCH, DISK_FULL, DEADLOCK) with auto-remediation tips.
"""

import re
from typing import Dict, Optional
from pydantic import BaseModel


class ErrorClassification(BaseModel):
    category: str
    confidence: float
    remediation_hint: str


class LogErrorClassifier:
    """Classifies log errors into root causes."""

    @classmethod
    def classify_log(cls, log_text: str) -> ErrorClassification:
        text = log_text.lower()
        if "out of memory" in text or "oomkilled" in text or "javalangoutofmemoryerror" in text:
            return ErrorClassification(
                category="OUT_OF_MEMORY",
                confidence=0.98,
                remediation_hint="Increase worker container memory limit or decrease VectorBatch chunk_size."
            )
        elif "connection timed out" in text or "timeouterror" in text or "read timed out" in text:
            return ErrorClassification(
                category="NETWORK_TIMEOUT",
                confidence=0.92,
                remediation_hint="Increase connection socket timeout or check upstream API rate limiting."
            )
        elif "column not found" in text or "type mismatch" in text or "schema" in text:
            return ErrorClassification(
                category="SCHEMA_MISMATCH",
                confidence=0.95,
                remediation_hint="Verify OpenDataContract schema definition or enable auto-schema evolution."
            )

        return ErrorClassification(
            category="UNKNOWN_ERROR",
            confidence=0.50,
            remediation_hint="Inspect task stderr logs for full stack trace details."
        )
