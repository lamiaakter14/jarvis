"""API v2 - Enhanced Cognitive Loop."""
from fastapi import APIRouter

from jarvis_core.orchestrator.loop import CognitiveOrchestrator
from .endpoints import cognitive_loop

router = APIRouter()

# Include cognitive loop endpoints
router.include_router(cognitive_loop.router, tags=["cognitive-loop"])


@router.get("/")
async def v2_root():
    """V2 API root endpoint."""
    return {
        "message": "API v2 - Cognitive Loop System",
        "status": "active",
        "endpoints": {
            "cognitive_loop": "/v2/cognitive-loop/run",
            "health": "/v2/cognitive-loop/health"
        }
    }
