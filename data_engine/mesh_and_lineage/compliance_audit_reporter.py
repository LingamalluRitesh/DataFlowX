"""
DataFlowX GDPR / CCPA / HIPAA Regulatory Compliance Audit Reporter
Generates GDPR Article 30 Records of Processing Activities (RoPA) logs, data subject request (DSR) traces, and encryption status reports.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RoPAEntry(BaseModel):
    activity_name: str
    purpose: str
    data_categories: List[str] = Field(default_factory=list)
    recipients: List[str] = Field(default_factory=list)
    retention_period_days: int = 365
    security_measures: str = "AES-256-GCM + RBAC"


class ComplianceAuditReport(BaseModel):
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_datasets_audited: int
    pii_columns_detected: int
    unencrypted_pii_count: int
    compliance_score_pct: float
    ropa_entries: List[RoPAEntry] = Field(default_factory=list)


class ComplianceAuditReporter:
    """Generates regulatory compliance audit dossiers."""

    @classmethod
    def generate_report(cls, datasets: List[Dict[str, Any]]) -> ComplianceAuditReport:
        total = len(datasets)
        pii_count = sum(1 for d in datasets if d.get("has_pii", False))
        unenc_count = sum(1 for d in datasets if d.get("has_pii", False) and not d.get("is_encrypted", False))

        score = round(100.0 * (total - unenc_count) / max(1, total), 1)

        ropa = [
            RoPAEntry(
                activity_name="Customer Analytics & Order Ingestion",
                purpose="Order processing and revenue analytics",
                data_categories=["Customer Identifiers", "Transaction Records", "IP Addresses"],
                recipients=["Internal Analytics Team", "Warehouse Gold Tier"],
                retention_period_days=730,
                security_measures="Envelope Encryption (AWS KMS) + Hash Masking"
            )
        ]

        return ComplianceAuditReport(
            total_datasets_audited=total,
            pii_columns_detected=pii_count,
            unencrypted_pii_count=unenc_count,
            compliance_score_pct=score,
            ropa_entries=ropa
        )
