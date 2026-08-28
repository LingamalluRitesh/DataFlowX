"""
DataFlowX Organization, Workspace & Team Service
"""

from typing import List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.exceptions import ConflictError, NotFoundError
from backend.database.models import Organization, Team, User, Workspace, WorkspaceMember
from backend.schemas.common import PaginationParams
from backend.schemas.organization import OrganizationCreate, OrganizationUpdate, WorkspaceCreate, WorkspaceUpdate


class OrganizationService:
    """Multi-tenancy and Workspace management."""

    @staticmethod
    async def list_organizations(session: AsyncSession, params: PaginationParams) -> Tuple[List[Organization], int]:
        query = select(Organization).where(Organization.is_deleted == False)
        if params.search:
            s = f"%{params.search}%"
            query = query.where(Organization.name.ilike(s))

        total_stmt = select(func.count()).select_from(query.subquery())
        total = (await session.execute(total_stmt)).scalar() or 0

        query = query.order_by(Organization.created_at.desc()).offset((params.page - 1) * params.page_size).limit(params.page_size)
        items = (await session.execute(query)).scalars().all()
        return list(items), total

    @staticmethod
    async def get_organization(session: AsyncSession, org_id: str) -> Organization:
        org = (await session.execute(select(Organization).where(Organization.id == org_id, Organization.is_deleted == False))).scalar_one_or_none()
        if not org:
            raise NotFoundError("Organization", org_id)
        return org

    @staticmethod
    async def create_organization(session: AsyncSession, payload: OrganizationCreate) -> Organization:
        slug = payload.slug or payload.name.lower().replace(" ", "-")
        org = Organization(
            name=payload.name,
            slug=slug,
            logo_url=payload.logo_url,
            plan=payload.plan,
            settings=payload.settings or {}
        )
        session.add(org)
        await session.flush()

        # Create default workspace
        ws = Workspace(
            organization_id=org.id,
            name="Default Workspace",
            slug="default",
            is_default=True
        )
        session.add(ws)
        await session.commit()
        await session.refresh(org)
        return org

    @staticmethod
    async def list_workspaces(session: AsyncSession, org_id: str) -> List[Workspace]:
        stmt = select(Workspace).where(Workspace.organization_id == org_id, Workspace.is_deleted == False)
        workspaces = (await session.execute(stmt)).scalars().all()
        return list(workspaces)

    @staticmethod
    async def create_workspace(session: AsyncSession, org_id: str, payload: WorkspaceCreate) -> Workspace:
        slug = payload.slug or payload.name.lower().replace(" ", "-")
        ws = Workspace(
            organization_id=org_id,
            name=payload.name,
            slug=slug,
            description=payload.description,
            settings=payload.settings or {}
        )
        session.add(ws)
        await session.commit()
        await session.refresh(ws)
        return ws
