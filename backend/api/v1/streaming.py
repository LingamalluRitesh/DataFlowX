"""
Real-Time Streaming Pipelines REST API Endpoints
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends

from backend.api.v1.deps import get_current_user
from backend.database.models.user import User
from backend.services.stream_service import StreamingPipelineInfo, StreamService

router = APIRouter(prefix="/streaming", tags=["Real-Time Streaming"])


@router.get("/pipelines", response_model=List[StreamingPipelineInfo])
async def list_streaming_pipelines(
    current_user: User = Depends(get_current_user)
) -> Any:
    """List all real-time micro-batch streaming pipelines."""
    return await StreamService.list_streaming_pipelines()
