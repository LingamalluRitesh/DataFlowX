"""
DataFlowX Privacy Compliance & PII Scanning Service
"""

from typing import Any, Dict, List, Optional
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.logging import get_logger
from data_engine.governance.privacy_compliance import PrivacyComplianceScanner, PrivacyScanReport

logger = get_logger(__name__)


class PrivacyService:
    """Service for running automated GDPR/CCPA scans and PII classifications."""

    @staticmethod
    async def scan_dataset_sample(
        dataset_name: str,
        sample_records: List[Dict[str, Any]]
    ) -> PrivacyScanReport:
        df = pd.DataFrame(sample_records) if sample_records else pd.DataFrame()
        report = PrivacyComplianceScanner.scan_dataframe(df, dataset_name=dataset_name)
        logger.info(f"Scanned dataset '{dataset_name}' for PII: {len(report.pii_columns_detected)} sensitive fields identified")
        return report
