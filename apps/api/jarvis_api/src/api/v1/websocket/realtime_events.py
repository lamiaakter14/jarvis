"""WebSocket endpoint for real-time events."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from datetime import datetime
from .connection_manager import manager


router = APIRouter()


@router.websocket("/ws/events/{client_id}")
async def realtime_events(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time system events."""
    await manager.connect(websocket, client_id)
    
    try:
        # Send welcome message
        await manager.send_json({
            "type": "connection",
            "message": "Connected to event stream",
            "client_id": client_id,
            "timestamp": datetime.utcnow().isoformat()
        }, websocket)
        
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Echo back for now
            await manager.send_json({
                "type": "event",
                "data": message,
                "timestamp": datetime.utcnow().isoformat()
            }, websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await manager.send_json({
            "type": "error",
            "message": str(e)
        }, websocket)
        manager.disconnect(websocket)
