"""Amplifier agent endpoints."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

try:
    from jarvis_core.bridge.agent_bridge import AmplifierBridge
except ImportError:
    AmplifierBridge = None


router = APIRouter()


@router.get("/performance")
async def get_performance() -> Dict[str, Any]:
    """Get performance metrics."""
    try:
        if not AmplifierBridge:
            raise HTTPException(status_code=503, detail="Amplifier bridge not available")
        
        amplifier = AmplifierBridge()
        performance = amplifier.amplify()
        return {
            "status": "success",
            "performance": performance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get performance: {str(e)}")
