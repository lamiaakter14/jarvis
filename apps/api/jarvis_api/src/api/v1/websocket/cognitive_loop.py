"""WebSocket endpoint for real-time cognitive loop updates."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import asyncio
from .connection_manager import manager


router = APIRouter()


@router.websocket("/ws/cognitive-loop/{client_id}")
async def cognitive_loop_websocket(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time cognitive loop updates."""
    await manager.connect(websocket, client_id)
    
    try:
        # Send welcome message
        await manager.send_json({
            "type": "connection",
            "message": "Connected to cognitive loop stream",
            "client_id": client_id
        }, websocket)
        
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await manager.send_json({
                    "type": "pong",
                    "timestamp": message.get("timestamp")
                }, websocket)
            
            elif message.get("type") == "start_loop":
                # Simulate cognitive loop execution
                await manager.send_json({
                    "type": "loop_started",
                    "message": "Cognitive loop execution started"
                }, websocket)
                
                # Simulate progress updates
                agents = ["strategist", "mentor", "executor", "innovator", "amplifier"]
                for i, agent in enumerate(agents):
                    await asyncio.sleep(1)
                    await manager.send_json({
                        "type": "agent_progress",
                        "agent": agent,
                        "progress": (i + 1) / len(agents) * 100,
                        "status": "processing"
                    }, websocket)
                
                await manager.send_json({
                    "type": "loop_completed",
                    "message": "Cognitive loop execution completed"
                }, websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await manager.send_json({
            "type": "error",
            "message": str(e)
        }, websocket)
        manager.disconnect(websocket)
