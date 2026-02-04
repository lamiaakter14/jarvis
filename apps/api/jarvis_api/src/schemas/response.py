"""Response schemas."""
from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel


T = TypeVar('T')


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response."""
    success: bool = True
    data: T
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: str
    details: Optional[Any] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: str
