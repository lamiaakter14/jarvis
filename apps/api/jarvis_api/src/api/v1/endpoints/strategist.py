"""Strategist agent endpoints."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

try:
    from jarvis_core.bridge.agent_bridge import StrategistBridge
except ImportError:
    StrategistBridge = None


router = APIRouter()


@router.get("/plan/today")
async def get_daily_plan() -> Dict[str, Any]:
    """Get today's daily plan."""
    try:
        if not StrategistBridge:
            raise HTTPException(status_code=503, detail="Strategist bridge not available")
        
        strategist = StrategistBridge()
        plan = strategist.generate_plan()
        return {
            "status": "success",
            "plan": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate plan: {str(e)}")
