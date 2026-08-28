"""
DataFlowX Users, Roles & API Keys Endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.deps import get_async_db, get_current_user, require_permission
from backend.database.models import User
from backend.schemas.common import PaginatedResponse, PaginationParams, StatusMessage
from backend.schemas.user import (
    ApiKeyCreate,
    ApiKeyOut,
    PermissionOut,
    RoleOut,
    UserCreate,
    UserOut,
    UserUpdate,
)
from backend.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users & RBAC"])


@router.get("", response_model=PaginatedResponse[UserOut])
async def list_users(
    page: int = 1,
    page_size: int = 20,
    search: str = None,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size, search=search)
    users, total = await UserService.list_users(session, params)
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    return PaginatedResponse(
        items=[UserOut.model_validate(u) for u in users],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=(page < total_pages),
        has_prev=(page > 1)
    )


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    user = await UserService.create_user(session, payload)
    return UserOut.model_validate(user)


@router.get("/roles", response_model=List[RoleOut])
async def list_roles(session: AsyncSession = Depends(get_async_db), _: User = Depends(get_current_user)):
    roles = await UserService.list_roles(session)
    return [RoleOut.model_validate(r) for r in roles]


@router.get("/permissions", response_model=List[PermissionOut])
async def list_permissions(session: AsyncSession = Depends(get_async_db), _: User = Depends(get_current_user)):
    perms = await UserService.list_permissions(session)
    return [PermissionOut.model_validate(p) for p in perms]


@router.post("/api-keys", response_model=ApiKeyOut, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    payload: ApiKeyCreate,
    session: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    api_key, raw_key = await UserService.create_api_key(session, current_user.id, payload)
    out = ApiKeyOut.model_validate(api_key)
    out.raw_key = raw_key
    return out
