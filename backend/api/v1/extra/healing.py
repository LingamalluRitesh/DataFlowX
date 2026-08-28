from typing import Any, Dict, List, Optional
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel

from backend.services.extra.healing_service import HealingService

router = APIRouter(prefix="/healing", tags=["Auto-Healing"])


class HealingTriggerRequest(BaseModel):
    impute_columns: Optional[Dict[str, str]] = None
    quarantine_columns: Optional[List[str]] = None


@router.post("/execute")
def trigger_healing(req: HealingTriggerRequest) -> Dict[str, Any]:
    sample_df = pd.DataFrame({
        "order_id": [1, None, 3, 4],
        "order_total": [100.0, 50.0, None, 200.0]
    })
    clean_df, dlq_df, result = HealingService.execute_dataset_healing(
        sample_df,
        impute_map=req.impute_columns,
        quarantine_cols=req.quarantine_columns
    )
    return {
        "status": "SUCCESS",
        "result": result.dict(),
        "clean_sample": clean_df.to_dict(orient="records"),
        "dlq_sample": dlq_df.to_dict(orient="records")
    }
