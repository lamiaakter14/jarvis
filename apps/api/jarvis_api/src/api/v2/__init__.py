"""API v2 placeholder - Future API version."""
from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def v2_root():
    """V2 API root endpoint."""
    return {
        "message": "API v2 - Coming soon",
        "status": "under_development"
    }
