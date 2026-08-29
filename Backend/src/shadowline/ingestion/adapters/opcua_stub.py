"""OPC-UA Ingestion Adapter Stub.

Architectural Rule (Constraint 1): Read-only, always.
Real industrial OPC-UA servers expose node hierarchies for station states, cycle metrics,
and error registers. This adapter connects to the OPC-UA endpoint with read-only subscriptions.
Zero write capabilities, methods, or client permissions exist.
"""

from datetime import datetime, timezone
import logging
from typing import Any, AsyncGenerator, Dict, Optional

from shadowline.domain.events import CanonicalEvent
from shadowline.ingestion.port import IngestionPort

logger = logging.getLogger("shadowline.ingestion.opcua_stub")


class OpcUaIngestionStub(IngestionPort):
    """Stub documenting the production OPC-UA read-only subscription path."""

    def __init__(self, endpoint_url: str = "opc.tcp://plant-gateway.local:4840", namespace_index: int = 2):
        self.endpoint_url = endpoint_url
        self.namespace_index = namespace_index
        self.is_connected = False
        self._events_read = 0

    async def start(self) -> None:
        logger.info("Initializing read-only OPC-UA client connection to %s", self.endpoint_url)
        # Production implementation initializes opcua-asyncio ReadOnlyClient
        self.is_connected = True

    async def stop(self) -> None:
        logger.info("Closing OPC-UA client connection.")
        self.is_connected = False

    async def stream_events(self) -> AsyncGenerator[CanonicalEvent, None]:
        """Subscribes read-only to MonitoredItem changes on OPC-UA NodeIds."""
        # Yield nothing in stub mode
        if False:
            yield None

    async def get_health(self) -> Dict[str, Any]:
        return {
            "adapter": "opcua_stub",
            "endpoint_url": self.endpoint_url,
            "is_connected": self.is_connected,
            "events_read": self._events_read,
            "read_only_verified": True,
        }
