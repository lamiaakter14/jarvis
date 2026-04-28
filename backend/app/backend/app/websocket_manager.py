

from fastapi import WebSocket
from typing import List, Dict, Any
import json
import asyncio
from datetime import datetime, timezone

class ConnectionManager:
    """
    WebSocket connection manager for cognitive loop streaming.
    Maintains active connections and broadcasts agent events.
    """
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self._loop_task = None
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # Send initial connection confirmation
        await self.send_personal_message({
            "type": "connection_established",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "active_connections": len(self.active_connections),
            "message": "Connected to JARVIS cognitive loop"
        }, websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def broadcast(self, event: Dict[str, Any]):
        """Broadcast cognitive event to all connected clients."""
        dead_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(event))
            except Exception:
                dead_connections.append(connection)
        
        # Clean up dead connections
        for dead in dead_connections:
            self.active_connections.remove(dead)
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send message to specific client."""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception:
            self.disconnect(websocket)

# Singleton instance
manager = ConnectionManager()