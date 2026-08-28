"""
DataFlowX Authentication API Endpoints
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.deps import get_current_user, get_async_db
from backend.database.models import User
from backend.schemas.auth import (
    RefreshTokenRequest,
    TokenResponse,
    UserLogin,
    UserRegister,
    UserSessionInfo,
)
from backend.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegister, session: AsyncSession = Depends(get_async_db)):
    """Register a new user account and receive authentication tokens."""
    _, tokens = await AuthService.register(session, payload)
    return tokens


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, session: AsyncSession = Depends(get_async_db)):
    """Authenticate user with username/email and password."""
    return await AuthService.login(session, payload)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(payload: RefreshTokenRequest, session: AsyncSession = Depends(get_async_db)):
    """Rotate and refresh access token with a valid refresh token."""
    return await AuthService.refresh_token(session, payload.refresh_token)


@router.get("/me", response_model=UserSessionInfo)
async def get_current_profile(current_user: User = Depends(get_current_user)):
    """Return currently authenticated user identity and claims."""
    return UserSessionInfo(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_superuser=current_user.is_superuser,
        is_active=current_user.is_active,
        roles=["admin"] if current_user.is_superuser else ["data_engineer"],
        permissions=["*"] if current_user.is_superuser else ["read", "write"]
    )
