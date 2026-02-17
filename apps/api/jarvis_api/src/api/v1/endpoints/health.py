"""Health check endpoint."""

from datetime import datetime

from fastapi import APIRouter

from ...config.settings import settings
from ...schemas.response import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy", version=settings.app_version, timestamp=datetime.utcnow().isoformat()
    )
