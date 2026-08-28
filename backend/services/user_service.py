"""
DataFlowX User & RBAC Service
"""

from typing import List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.exceptions import ConflictError, NotFoundError
from backend.core.security import generate_api_key, get_password_hash
from backend.database.models import ApiKey, Permission, Role, RolePermission, User, UserRole
from backend.schemas.common import PaginationParams
from backend.schemas.user import ApiKeyCreate, RoleCreate, RoleUpdate, UserCreate, UserUpdate


class UserService:
    """User and Role-based Access Control business logic."""

    @staticmethod
    async def list_users(session: AsyncSession, params: PaginationParams) -> Tuple[List[User], int]:
        query = select(User).where(User.is_deleted == False)
        if params.search:
            s = f"%{params.search}%"
            query = query.where((User.email.ilike(s)) | (User.username.ilike(s)) | (User.full_name.ilike(s)))

        total_stmt = select(func.count()).select_from(query.subquery())
        total = (await session.execute(total_stmt)).scalar() or 0

        query = query.order_by(User.created_at.desc()).offset((params.page - 1) * params.page_size).limit(params.page_size)
        items = (await session.execute(query)).scalars().all()
        return list(items), total

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: str) -> User:
        user = (await session.execute(select(User).where(User.id == user_id, User.is_deleted == False))).scalar_one_or_none()
        if not user:
            raise NotFoundError("User", user_id)
        return user

    @staticmethod
    async def create_user(session: AsyncSession, payload: UserCreate) -> User:
        stmt = select(User).where((User.email == payload.email) | (User.username == payload.username))
        existing = (await session.execute(stmt)).scalar_one_or_none()
        if existing:
            raise ConflictError("User with this email or username already exists")

        user = User(
            email=payload.email,
            username=payload.username,
            hashed_password=get_password_hash(payload.password),
            full_name=payload.full_name,
            is_active=payload.is_active,
            is_superuser=payload.is_superuser,
            avatar_url=payload.avatar_url,
            is_verified=True
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def update_user(session: AsyncSession, user_id: str, payload: UserUpdate) -> User:
        user = await UserService.get_user_by_id(session, user_id)
        if payload.full_name is not None:
            user.full_name = payload.full_name
        if payload.email is not None:
            user.email = payload.email
        if payload.is_active is not None:
            user.is_active = payload.is_active
        if payload.avatar_url is not None:
            user.avatar_url = payload.avatar_url

        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def delete_user(session: AsyncSession, user_id: str) -> None:
        user = await UserService.get_user_by_id(session, user_id)
        user.soft_delete()
        await session.commit()

    @staticmethod
    async def list_roles(session: AsyncSession) -> List[Role]:
        roles = (await session.execute(select(Role).order_by(Role.name))).scalars().all()
        return list(roles)

    @staticmethod
    async def list_permissions(session: AsyncSession) -> List[Permission]:
        perms = (await session.execute(select(Permission).order_by(Permission.module, Permission.code))).scalars().all()
        return list(perms)

    @staticmethod
    async def create_api_key(session: AsyncSession, user_id: str, payload: ApiKeyCreate) -> Tuple[ApiKey, str]:
        raw_key = generate_api_key()
        prefix = raw_key[:12]
        key_hash = get_password_hash(raw_key)

        api_key = ApiKey(
            user_id=user_id,
            name=payload.name,
            prefix=prefix,
            key_hash=key_hash,
            is_active=True
        )
        session.add(api_key)
        await session.commit()
        await session.refresh(api_key)
        return api_key, raw_key
