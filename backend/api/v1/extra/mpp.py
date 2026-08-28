from typing import Any, Dict, Optional
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel

from backend.services.extra.mpp_service import VectorizedMPPService

router = APIRouter(prefix="/mpp", tags=["Vectorized MPP Engine"])
_service = VectorizedMPPService()


class MPPQueryExecuteRequest(BaseModel):
    filter_column: Optional[str] = None
    filter_value: Optional[str] = None


@router.post("/execute")
def execute_vector_query(req: MPPQueryExecuteRequest) -> Dict[str, Any]:
    df = pd.DataFrame({
        "order_id": [1, 2, 3, 4],
        "status": ["COMPLETED", "PENDING", "COMPLETED", "SHIPPED"],
        "amount": [120.5, 45.0, 99.0, 310.0]
    })
    res_df, profile = _service.run_query(df, req.filter_column, req.filter_value)
    return {
        "status": "SUCCESS",
        "profile": profile.dict(),
        "rows_returned": len(res_df),
        "data": res_df.to_dict(orient="records")
    }
