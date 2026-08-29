"""WebSocket connection manager."""

import asyncio
import json
import logging
from typing import Any, Dict, List, Set
from fastapi import WebSocket

logger = logging.getLogger("shadowline.api.ws.manager")


class WebSocketConnectionManager:
    """Manages active client WebSocket connections and broadcasts real-time telemetry."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self.active_connections.add(websocket)
        logger.info("WebSocket client connected. Active: %d", len(self.active_connections))

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self.active_connections.discard(websocket)
        logger.info("WebSocket client disconnected. Active: %d", len(self.active_connections))

    async def broadcast(self, message: Dict[str, Any]) -> None:
        if not self.active_connections:
            return

        payload = json.dumps(message)
        dead_connections = set()

        async with self._lock:
            for conn in self.active_connections:
                try:
                    await conn.send_text(payload)
                except Exception:
                    dead_connections.add(conn)

            for dead in dead_connections:
                self.active_connections.discard(dead)


# Global WebSocket connection manager singleton
ws_manager = WebSocketConnectionManager()
