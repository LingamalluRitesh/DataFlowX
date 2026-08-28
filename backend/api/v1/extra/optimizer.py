from typing import Any, Dict
from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.extra.optimizer_service import OptimizerService

router = APIRouter(prefix="/optimizer", tags=["Query Optimizer"])
_service = OptimizerService()


class QueryOptimizeRequest(BaseModel):
    sql_query: str


@router.post("/optimize")
def optimize_sql_plan(req: QueryOptimizeRequest) -> Dict[str, Any]:
    summary = _service.optimize_query_plan(req.sql_query)
    return {"status": "SUCCESS", "optimization_summary": summary.dict()}
