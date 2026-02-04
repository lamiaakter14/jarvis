"""Health check endpoint."""
from fastapi import APIRouter
from datetime import datetime
from ...schemas.response import HealthResponse
from ...config.settings import settings


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.utcnow().isoformat()
    )
