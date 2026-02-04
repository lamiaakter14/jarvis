"""WebSocket connection manager."""
from typing import List, Dict
from fastapi import WebSocket


class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.client_data: Dict[WebSocket, dict] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str = None):
        """Accept and track a WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        if client_id:
            self.client_data[websocket] = {"client_id": client_id}
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.client_data:
            del self.client_data[websocket]
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific client."""
        await websocket.send_text(message)
    
    async def send_json(self, data: dict, websocket: WebSocket):
        """Send JSON data to a specific client."""
        await websocket.send_json(data)
    
    async def broadcast(self, message: str):
        """Broadcast a message to all connected clients."""
        for connection in self.active_connections:
            await connection.send_text(message)
    
    async def broadcast_json(self, data: dict):
        """Broadcast JSON data to all connected clients."""
        for connection in self.active_connections:
            await connection.send_json(data)


manager = ConnectionManager()
