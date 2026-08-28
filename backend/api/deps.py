"""
DataFlowX FastAPI Request Dependencies
Provides Current User resolution, RBAC permission verification, and Database session injection.
"""

from typing import AsyncGenerator, Callable, List, Optional
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.database import get_async_db
from backend.core.exceptions import AuthenticationError, PermissionDeniedError
from backend.core.jwt import TokenPayload, decode_token
from backend.database.models import User, Workspace, WorkspaceMember

security_scheme = HTTPBearer(auto_error=False)


async def get_current_token_payload(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
) -> TokenPayload:
    """Extract and validate JWT token from Bearer header."""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_token(credentials.credentials)
        return payload
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired authentication token: {str(exc)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    payload: TokenPayload = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_db),
) -> User:
    """Resolve active database User from token payload."""
    stmt = select(User).where(User.id == payload.sub, User.is_deleted == False)
    user = (await session.execute(stmt)).scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account does not exist or has been disabled",
        )
    return user


def require_permission(required_perm: str) -> Callable:
    """Dependency enforcing a specific RBAC permission."""
    async def permission_checker(
        payload: TokenPayload = Depends(get_current_token_payload),
        user: User = Depends(get_current_user),
    ) -> User:
        if user.is_superuser or "*" in payload.permissions:
            return user
        if required_perm not in payload.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User lacks required permission: '{required_perm}'"
            )
        return user
    return permission_checker


async def get_active_workspace_id(
    payload: TokenPayload = Depends(get_current_token_payload),
    x_workspace_id: Optional[str] = Header(None, alias="X-Workspace-ID")
) -> Optional[str]:
    """Resolve active workspace ID from header or JWT claim."""
    return x_workspace_id or payload.workspace_id
