"""Mentor agent endpoints."""

from typing import Any, Dict

from fastapi import APIRouter, HTTPException

try:
    from jarvis_core.bridge.agent_bridge import MentorBridge
except ImportError:
    MentorBridge = None


router = APIRouter()


@router.get("/gaps")
async def get_knowledge_gaps() -> Dict[str, Any]:
    """Get identified knowledge gaps."""
    try:
        if not MentorBridge:
            raise HTTPException(status_code=503, detail="Mentor bridge not available")

        mentor = MentorBridge()
        gaps = mentor.analyze_execution_logs()
        return {"status": "success", "gaps": gaps}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze gaps: {str(e)}")
