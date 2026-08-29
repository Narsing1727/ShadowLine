"""WebSocket live push feed endpoint."""

import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from shadowline.api.ws.connection_manager import ws_manager

logger = logging.getLogger("shadowline.api.ws.live_feed")
ws_router = APIRouter()


@ws_router.websocket("/ws/live")
async def websocket_live_feed(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            # Client can send keepalives or query commands
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error("WebSocket live feed error: %s", e)
        await ws_manager.disconnect(websocket)
