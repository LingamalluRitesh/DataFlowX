"""
DataFlowX Compliance Frameworks Control Matrix
Implements automated audit evaluation controls for GDPR, CCPA, HIPAA, SOX, and PCI-DSS compliance requirements.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ComplianceControlCheck(BaseModel):
    control_id: str
    framework: str  # GDPR, CCPA, HIPAA, SOX, PCI_DSS
    title: str
    description: str
    passed: bool
    remediation_guidance: Optional[str] = None


class ComplianceAssessment(BaseModel):
    framework: str
    overall_compliance_pct: float
    passed_controls_count: int
    total_controls_count: int
    controls: List[ComplianceControlCheck] = Field(default_factory=list)


class ComplianceAuditor:
    """Evaluates workspace security settings and datasets against global compliance controls."""

    @staticmethod
    def audit_gdpr_compliance(has_unmasked_pii: bool, has_audit_logging: bool, retention_days_configured: bool) -> ComplianceAssessment:
        controls = [
            ComplianceControlCheck(
                control_id="GDPR-Art-32",
                framework="GDPR",
                title="Security of processing (Pseudonymisation and Encryption)",
                passed=not has_unmasked_pii,
                remediation_guidance="Enable SaltedHashTokenizeOperator on cleartext PII columns." if has_unmasked_pii else None
            ),
            ComplianceControlCheck(
                control_id="GDPR-Art-30",
                framework="GDPR",
                title="Records of processing activities (Audit Logging)",
                passed=has_audit_logging,
                remediation_guidance="Activate immutable audit log emitter in platform settings." if not has_audit_logging else None
            ),
            ComplianceControlCheck(
                control_id="GDPR-Art-5-1e",
                framework="GDPR",
                title="Storage limitation (Data Retention Policy)",
                passed=retention_days_configured,
                remediation_guidance="Define TTL partition expiry policy on bronze storage buckets." if not retention_days_configured else None
            )
        ]

        passed_cnt = sum(1 for c in controls if c.passed)
        pct = round((passed_cnt / len(controls)) * 100, 2)

        return ComplianceAssessment(
            framework="GDPR",
            overall_compliance_pct=pct,
            passed_controls_count=passed_cnt,
            total_controls_count=len(controls),
            controls=controls
        )
