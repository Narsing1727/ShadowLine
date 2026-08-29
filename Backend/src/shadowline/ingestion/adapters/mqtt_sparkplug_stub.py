"""MQTT Sparkplug B Ingestion Adapter Stub.

Architectural Rule (Constraint 1): Read-only, always.
Sparkplug B defines edge payload structures (NBIRTH, NDATA, DDATA, DDEATH).
This adapter subscribes to telemetry topics (`spBv1.0/+/NDATA/+` and `spBv1.0/+/DDATA/+/+`).
It never issues NCMD or DCMD write commands to control units.
"""

from datetime import datetime, timezone
import logging
from typing import Any, AsyncGenerator, Dict, Optional

from shadowline.domain.events import CanonicalEvent
from shadowline.ingestion.port import IngestionPort

logger = logging.getLogger("shadowline.ingestion.mqtt_sparkplug_stub")


class MqttSparkplugStub(IngestionPort):
    """Stub documenting the production MQTT Sparkplug B read-only subscriber path."""

    def __init__(self, broker_host: str = "mqtt-broker.local", broker_port: int = 1883, group_id: str = "Plant2"):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.group_id = group_id
        self.is_connected = False
        self._metrics_received = 0

    async def start(self) -> None:
        logger.info("Initializing read-only MQTT Sparkplug subscriber to %s:%d", self.broker_host, self.broker_port)
        self.is_connected = True

    async def stop(self) -> None:
        logger.info("Closing MQTT subscriber.")
        self.is_connected = False

    async def stream_events(self) -> AsyncGenerator[CanonicalEvent, None]:
        # Yield nothing in stub mode
        if False:
            yield None

    async def get_health(self) -> Dict[str, Any]:
        return {
            "adapter": "mqtt_sparkplug_stub",
            "broker": f"{self.broker_host}:{self.broker_port}",
            "group_id": self.group_id,
            "is_connected": self.is_connected,
            "metrics_received": self._metrics_received,
            "read_only_verified": True,
        }
