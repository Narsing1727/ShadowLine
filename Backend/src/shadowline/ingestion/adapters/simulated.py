"""Simulated ingestion adapter consuming events emitted by sim_plant or test drivers.

Architectural Rule: Never imports from sim_plant.
"""

import asyncio
from datetime import datetime, timezone
import logging
from typing import Any, AsyncGenerator, Dict, List, Optional
import httpx

from shadowline.domain.events import CanonicalEvent
from shadowline.ingestion.normalizer import EventNormalizer
from shadowline.ingestion.port import IngestionPort

logger = logging.getLogger("shadowline.ingestion.simulated")


class SimulatedIngestionAdapter(IngestionPort):
    """Consumes events from sim_plant HTTP/SSE feed or internal async queues."""

    def __init__(self, endpoint_url: str = "http://localhost:8100/events", poll_interval: float = 0.5):
        self.endpoint_url = endpoint_url
        self.poll_interval = poll_interval
        self.is_running = False
        self._queue: asyncio.Queue[CanonicalEvent] = asyncio.Queue()
        self._events_ingested = 0
        self._last_event_time: Optional[datetime] = None

    async def start(self) -> None:
        self.is_running = True
        logger.info("Simulated ingestion adapter started.")

    async def stop(self) -> None:
        self.is_running = False
        logger.info("Simulated ingestion adapter stopped.")

    def inject_event(self, raw_event: Dict[str, Any]) -> None:
        """Allows direct injection of simulated raw event dicts (e.g. in test suites)."""
        event = EventNormalizer.normalize(raw_event, source="simulated")
        self._events_ingested += 1
        self._last_event_time = datetime.now(timezone.utc)
        self._queue.put_nowait(event)

    async def stream_events(self) -> AsyncGenerator[CanonicalEvent, None]:
        while self.is_running:
            try:
                # Wait for next available event in queue with timeout
                event = await asyncio.wait_for(self._queue.get(), timeout=self.poll_interval)
                yield event
            except asyncio.TimeoutError:
                # Polling heartbeat / yield control
                await asyncio.sleep(0.01)
                continue
            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.error("Error in simulated event stream: %s", exc)
                await asyncio.sleep(self.poll_interval)

    async def get_health(self) -> Dict[str, Any]:
        return {
            "adapter": "simulated",
            "is_running": self.is_running,
            "events_ingested": self._events_ingested,
            "queue_size": self._queue.qsize(),
            "last_event_time": self._last_event_time.isoformat() if self._last_event_time else None,
        }
