"""
DataFlowX Data Quality Service
Manages quality rule definitions, test suites, check executions, and quality metrics history.
"""

from typing import List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.exceptions import NotFoundError
from backend.database.models import QualityCheck, QualityResult, QualityRuleDefinition, QualitySuite
from backend.schemas.common import PaginationParams
from backend.schemas.quality import QualityCheckCreate, QualityRuleDefCreate, QualitySuiteCreate


class QualityService:
    """Data quality rules and test suite management."""

    @staticmethod
    async def list_suites(session: AsyncSession, workspace_id: Optional[str], params: PaginationParams) -> Tuple[List[QualitySuite], int]:
        query = select(QualitySuite).where(QualitySuite.is_deleted == False)
        if workspace_id:
            query = query.where(QualitySuite.workspace_id == workspace_id)
        if params.search:
            s = f"%{params.search}%"
            query = query.where(QualitySuite.name.ilike(s))

        total_stmt = select(func.count()).select_from(query.subquery())
        total = (await session.execute(total_stmt)).scalar() or 0

        query = query.order_by(QualitySuite.created_at.desc()).offset((params.page - 1) * params.page_size).limit(params.page_size)
        items = (await session.execute(query)).scalars().all()
        return list(items), total

    @staticmethod
    async def get_suite(session: AsyncSession, suite_id: str) -> QualitySuite:
        suite = (await session.execute(select(QualitySuite).where(QualitySuite.id == suite_id, QualitySuite.is_deleted == False))).scalar_one_or_none()
        if not suite:
            raise NotFoundError("QualitySuite", suite_id)
        return suite

    @staticmethod
    async def create_suite(session: AsyncSession, workspace_id: Optional[str], payload: QualitySuiteCreate) -> QualitySuite:
        suite = QualitySuite(
            workspace_id=workspace_id,
            name=payload.name,
            description=payload.description,
            is_active=payload.is_active
        )
        session.add(suite)
        await session.flush()

        for check_cfg in payload.checks:
            chk = QualityCheck(
                quality_suite_id=suite.id,
                rule_name=check_cfg.rule_name,
                rule_type=check_cfg.rule_type,
                target_column=check_cfg.target_column,
                condition_params=check_cfg.condition_params,
                threshold_percentage=check_cfg.threshold_percentage,
                failure_action=check_cfg.failure_action,
                is_enabled=check_cfg.is_enabled
            )
            session.add(chk)

        await session.commit()
        await session.refresh(suite)
        return suite

    @staticmethod
    async def list_rule_definitions(session: AsyncSession, workspace_id: Optional[str]) -> List[QualityRuleDefinition]:
        stmt = select(QualityRuleDefinition).where(
            (QualityRuleDefinition.is_builtin == True) | (QualityRuleDefinition.workspace_id == workspace_id)
        ).order_by(QualityRuleDefinition.name)
        rules = (await session.execute(stmt)).scalars().all()
        return list(rules)

    @staticmethod
    async def create_rule_definition(session: AsyncSession, workspace_id: Optional[str], payload: QualityRuleDefCreate) -> QualityRuleDefinition:
        rule = QualityRuleDefinition(
            workspace_id=workspace_id,
            name=payload.name,
            rule_type=payload.rule_type,
            description=payload.description,
            parameters_schema_json=payload.parameters_schema,
            default_severity=payload.default_severity,
            is_builtin=False
        )
        session.add(rule)
        await session.commit()
        await session.refresh(rule)
        return rule
