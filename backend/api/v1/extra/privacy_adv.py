from typing import Any, Dict, List, Optional
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel

from backend.services.extra.privacy_service_advanced import AdvancedPrivacyService

router = APIRouter(prefix="/privacy-adv", tags=["Advanced Privacy"])


class PrivacyAuditRequest(BaseModel):
    quasi_identifiers: List[str]
    sensitive_column: Optional[str] = None


@router.post("/audit")
def audit_privacy(req: PrivacyAuditRequest) -> Dict[str, Any]:
    sample_df = pd.DataFrame({
        "age_bracket": ["20-30", "20-30", "30-40", "30-40", "30-40"],
        "gender": ["M", "M", "F", "F", "F"],
        "diagnosis": ["Hypertension", "Asthma", "Diabetes", "Diabetes", "Hypertension"]
    })
    res = AdvancedPrivacyService.audit_dataset_privacy(sample_df, req.quasi_identifiers, req.sensitive_column)
    return {
        "status": "SUCCESS",
        "audit_results": {
            "k_anonymity": res["k_anonymity"].dict() if res["k_anonymity"] else None,
            "l_diversity": res["l_diversity"].dict() if res["l_diversity"] else None,
            "t_closeness": res["t_closeness"].dict() if res["t_closeness"] else None,
        }
    }
