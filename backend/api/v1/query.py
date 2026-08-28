"""
Interactive SQL Query REST API Endpoints
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.api.v1.deps import get_current_user
from backend.database.models.user import User
from backend.services.query_service import QueryExecutionResult, QueryService

router = APIRouter(prefix="/query", tags=["Interactive SQL Query Studio"])


class ExecuteQueryRequest(BaseModel):
    sql: str
    max_rows: int = 1000


@router.post("/execute", response_model=QueryExecutionResult)
async def execute_sql_query(
    payload: ExecuteQueryRequest,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Execute interactive SQL query across workspace data lake tables."""
    return await QueryService.execute_ad_hoc_query(sql=payload.sql, max_rows=payload.max_rows)
