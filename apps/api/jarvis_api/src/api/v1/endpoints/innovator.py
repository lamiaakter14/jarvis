"""Innovator agent endpoints."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

try:
    from jarvis_core.bridge.agent_bridge import InnovatorBridge
except ImportError:
    InnovatorBridge = None


router = APIRouter()


@router.get("/innovations")
async def get_innovations() -> Dict[str, Any]:
    """Get generated innovations."""
    try:
        if not InnovatorBridge:
            raise HTTPException(status_code=503, detail="Innovator bridge not available")
        
        innovator = InnovatorBridge()
        innovations = innovator.create_innovations()
        return {
            "status": "success",
            "innovations": innovations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate innovations: {str(e)}")
