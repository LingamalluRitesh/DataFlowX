"""
DataFlowX Authentication & Identity Service
Handles user registration, authentication, JWT tokens, password resets, and session management.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.config import settings
from backend.core.exceptions import AuthenticationError, ConflictError, NotFoundError, ValidationError
from backend.core.jwt import create_access_token, create_refresh_token, decode_token
from backend.core.logging import get_logger
from backend.core.security import get_password_hash, validate_password_strength, verify_password
from backend.database.models import (
    Organization,
    PasswordReset,
    Role,
    User,
    UserRole,
    UserSession,
    Workspace,
    WorkspaceMember,
)
from backend.schemas.auth import (
    ChangePassword,
    PasswordResetConfirm,
    TokenResponse,
    UserLogin,
    UserProfileUpdate,
    UserRegister,
    UserSessionInfo,
)

logger = get_logger(__name__)


class AuthService:
    """Enterprise authentication and session service."""

    @staticmethod
    async def register(session: AsyncSession, payload: UserRegister) -> Tuple[User, TokenResponse]:
        # Validate password strength
        is_strong, err = validate_password_strength(payload.password)
        if not is_strong:
            raise ValidationError(err or "Weak password")

        # Check existing email/username
        stmt = select(User).where((User.email == payload.email) | (User.username == payload.username))
        existing = (await session.execute(stmt)).scalar_one_or_none()
        if existing:
            raise ConflictError("User with this email or username already exists")

        # Create user
        hashed_pwd = get_password_hash(payload.password)
        user = User(
            email=payload.email,
            username=payload.username,
            hashed_password=hashed_pwd,
            full_name=payload.full_name,
            is_active=True,
            is_verified=True,
        )
        session.add(user)
        await session.flush()

        # Create default organization & workspace
        org_name = payload.organization_name or f"{payload.username}'s Org"
        org = Organization(
            name=org_name,
            slug=org_name.lower().replace(" ", "-"),
            plan="enterprise",
        )
        session.add(org)
        await session.flush()

        ws = Workspace(
            organization_id=org.id,
            name="Default Workspace",
            slug="default",
            is_default=True,
        )
        session.add(ws)
        await session.flush()

        # Add user as workspace member
        member = WorkspaceMember(
            workspace_id=ws.id,
            user_id=user.id,
            role_name="admin",
            status="active"
        )
        session.add(member)

        # Issue tokens
        access_token = create_access_token(
            user_id=user.id,
            email=user.email,
            username=user.username,
            organization_id=org.id,
            workspace_id=ws.id,
            roles=["admin"],
            permissions=["*"]
        )
        refresh_token = create_refresh_token(user_id=user.id, email=user.email, username=user.username)

        # Record session
        user_sess = UserSession(
            user_id=user.id,
            token_hash=get_password_hash(refresh_token[:30]),
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        session.add(user_sess)
        await session.commit()

        session_info = UserSessionInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_superuser=user.is_superuser,
            is_active=user.is_active,
            current_organization_id=org.id,
            current_workspace_id=ws.id,
            roles=["admin"],
            permissions=["*"]
        )

        tokens = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=session_info
        )

        logger.info(f"New user registered: {user.email}")
        return user, tokens

    @staticmethod
    async def login(session: AsyncSession, payload: UserLogin) -> TokenResponse:
        stmt = select(User).where(
            (User.email == payload.username_or_email) | (User.username == payload.username_or_email)
        )
        user = (await session.execute(stmt)).scalar_one_or_none()

        if not user or not verify_password(payload.password, user.hashed_password):
            raise AuthenticationError("Invalid username/email or password")

        if not user.is_active:
            raise AuthenticationError("Account is inactive or suspended")

        user.last_login_at = datetime.now(timezone.utc)

        # Retrieve user's primary workspace & org
        ws_stmt = select(WorkspaceMember).where(WorkspaceMember.user_id == user.id)
        ws_member = (await session.execute(ws_stmt)).scalar_one_or_none()

        org_id = None
        ws_id = None
        roles = ["data_engineer"]

        if ws_member:
            ws_id = ws_member.workspace_id
            ws = (await session.execute(select(Workspace).where(Workspace.id == ws_id))).scalar_one_or_none()
            if ws:
                org_id = ws.organization_id
            roles = [ws_member.role_name]
        elif user.is_superuser:
            roles = ["super_admin"]

        access_token = create_access_token(
            user_id=user.id,
            email=user.email,
            username=user.username,
            organization_id=org_id,
            workspace_id=ws_id,
            roles=roles,
            permissions=["*"] if user.is_superuser or "admin" in roles else ["read", "write"]
        )
        refresh_token = create_refresh_token(user_id=user.id, email=user.email, username=user.username)

        # Store session
        user_sess = UserSession(
            user_id=user.id,
            token_hash=get_password_hash(refresh_token[:30]),
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        session.add(user_sess)
        await session.commit()

        session_info = UserSessionInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_superuser=user.is_superuser,
            is_active=user.is_active,
            current_organization_id=org_id,
            current_workspace_id=ws_id,
            roles=roles,
            permissions=["*"] if user.is_superuser or "admin" in roles else ["read", "write"]
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=session_info
        )

    @staticmethod
    async def refresh_token(session: AsyncSession, refresh_token_str: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token_str)
            if payload.type != "refresh":
                raise AuthenticationError("Invalid token type")
        except Exception:
            raise AuthenticationError("Invalid or expired refresh token")

        user = (await session.execute(select(User).where(User.id == payload.sub))).scalar_one_or_none()
        if not user or not user.is_active:
            raise AuthenticationError("User not found or suspended")

        ws_member = (await session.execute(select(WorkspaceMember).where(WorkspaceMember.user_id == user.id))).scalar_one_or_none()
        org_id = None
        ws_id = None
        roles = ["data_engineer"]
        if ws_member:
            ws_id = ws_member.workspace_id
            ws = (await session.execute(select(Workspace).where(Workspace.id == ws_id))).scalar_one_or_none()
            if ws:
                org_id = ws.organization_id
            roles = [ws_member.role_name]

        new_access = create_access_token(
            user_id=user.id,
            email=user.email,
            username=user.username,
            organization_id=org_id,
            workspace_id=ws_id,
            roles=roles,
            permissions=["*"] if user.is_superuser or "admin" in roles else ["read", "write"]
        )
        new_refresh = create_refresh_token(user_id=user.id, email=user.email, username=user.username)

        session_info = UserSessionInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_superuser=user.is_superuser,
            is_active=user.is_active,
            current_organization_id=org_id,
            current_workspace_id=ws_id,
            roles=roles,
            permissions=["*"] if user.is_superuser or "admin" in roles else ["read", "write"]
        )

        return TokenResponse(
            access_token=new_access,
            refresh_token=new_refresh,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=session_info
        )
