"""API v1 router."""
from fastapi import APIRouter
from .endpoints import health, cognitive_loop, strategist, mentor, innovator, amplifier
from .websocket import cognitive_loop as ws_cognitive_loop, realtime_events


router = APIRouter()

# Include all endpoint routers
router.include_router(health.router, tags=["health"])
router.include_router(cognitive_loop.router, tags=["cognitive-loop"])
router.include_router(strategist.router, tags=["strategist"])
router.include_router(mentor.router, tags=["mentor"])
router.include_router(innovator.router, tags=["innovator"])
router.include_router(amplifier.router, tags=["amplifier"])

# Include WebSocket routers
router.include_router(ws_cognitive_loop.router, tags=["websocket"])
router.include_router(realtime_events.router, tags=["websocket"])
