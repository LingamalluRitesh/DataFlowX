"""
DataFlowX Data Quality API Endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.deps import get_active_workspace_id, get_async_db, get_current_user
from backend.database.models import User
from backend.schemas.common import PaginatedResponse, PaginationParams
from backend.schemas.quality import (
    QualityCheckOut,
    QualityRuleDefCreate,
    QualityRuleDefOut,
    QualitySuiteCreate,
    QualitySuiteOut,
)
from backend.services.quality_service import QualityService

router = APIRouter(prefix="/quality", tags=["Data Quality"])


@router.get("/rules", response_model=List[QualityRuleDefOut])
async def list_rule_definitions(
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    rules = await QualityService.list_rule_definitions(session, workspace_id)
    return [
        QualityRuleDefOut(
            id=r.id,
            name=r.name,
            rule_type=r.rule_type,
            description=r.description,
            parameters_schema=r.parameters_schema_json or {},
            default_severity=r.default_severity,
            is_builtin=r.is_builtin,
            created_at=r.created_at
        )
        for r in rules
    ]


@router.post("/rules", response_model=QualityRuleDefOut, status_code=status.HTTP_201_CREATED)
async def create_rule_definition(
    payload: QualityRuleDefCreate,
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    r = await QualityService.create_rule_definition(session, workspace_id, payload)
    return QualityRuleDefOut(
        id=r.id,
        name=r.name,
        rule_type=r.rule_type,
        description=r.description,
        parameters_schema=r.parameters_schema_json or {},
        default_severity=r.default_severity,
        is_builtin=r.is_builtin,
        created_at=r.created_at
    )


@router.get("/suites", response_model=PaginatedResponse[QualitySuiteOut])
async def list_suites(
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size, search=search)
    suites, total = await QualityService.list_suites(session, workspace_id, params)
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    return PaginatedResponse(
        items=[
            QualitySuiteOut(
                id=s.id,
                organization_id=s.organization_id,
                workspace_id=s.workspace_id,
                name=s.name,
                description=s.description,
                is_active=s.is_active,
                created_at=s.created_at,
                checks=[]
            )
            for s in suites
        ],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=(page < total_pages),
        has_prev=(page > 1)
    )


@router.post("/suites", response_model=QualitySuiteOut, status_code=status.HTTP_201_CREATED)
async def create_suite(
    payload: QualitySuiteCreate,
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    suite = await QualityService.create_suite(session, workspace_id, payload)
    return QualitySuiteOut(
        id=suite.id,
        organization_id=suite.organization_id,
        workspace_id=suite.workspace_id,
        name=suite.name,
        description=suite.description,
        is_active=suite.is_active,
        created_at=suite.created_at,
        checks=[]
    )
