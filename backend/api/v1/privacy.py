"""
Privacy and PII Scanner REST API Endpoints
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel

from backend.api.v1.deps import get_current_user
from backend.database.models.user import User
from backend.services.privacy_service import PrivacyService

router = APIRouter(prefix="/privacy", tags=["Privacy & GDPR/CCPA Compliance"])


class PrivacyScanRequest(BaseModel):
    dataset_name: str
    sample_records: List[Dict[str, Any]]


@router.post("/scan")
async def scan_dataset_privacy(
    payload: PrivacyScanRequest,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Execute automated PII classification scan on dataset records."""
    report = await PrivacyService.scan_dataset_sample(
        dataset_name=payload.dataset_name,
        sample_records=payload.sample_records
    )
    return report.dict()
