"""
DataFlowX Common Pydantic Schemas
Provides generic pagination wrappers, standard API responses, and filter params.
"""

from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Standard URL query pagination parameters."""
    page: int = Field(default=1, ge=1, description="Page number starting at 1")
    page_size: int = Field(default=20, ge=1, le=500, description="Number of items per page")
    search: Optional[str] = Field(default=None, description="Free text search query")
    sort_by: Optional[str] = Field(default="created_at", description="Field name to sort by")
    sort_order: Optional[str] = Field(default="desc", pattern="^(asc|desc)$", description="Sort direction")


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated collection response."""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

    model_config = ConfigDict(from_attributes=True)


class StandardResponse(BaseModel, Generic[T]):
    """Standard envelope response for single resource mutations."""
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[T] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class StatusMessage(BaseModel):
    """Simple status confirmation."""
    success: bool = True
    message: str
    code: Optional[str] = None
