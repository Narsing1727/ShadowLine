"""Transport layer for emitted simulation events."""

import asyncio
from typing import Any, Dict, List, Optional


class EventTransport:
    """In-memory async queue transport for simulated events."""

    def __init__(self, maxsize: int = 50000):
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=maxsize)
        self._history: List[Dict[str, Any]] = []

    async def publish(self, event_dict: Dict[str, Any]) -> None:
        self._history.append(event_dict)
        try:
            self.queue.put_nowait(event_dict)
        except asyncio.QueueFull:
            # Pop oldest to prevent hanging
            try:
                self.queue.get_nowait()
            except Exception:
                pass
            self.queue.put_nowait(event_dict)

    def publish_sync(self, event_dict: Dict[str, Any]) -> None:
        self._history.append(event_dict)
        try:
            self.queue.put_nowait(event_dict)
        except Exception:
            pass

    async def get(self) -> Dict[str, Any]:
        return await self.queue.get()

    def get_history(self) -> List[Dict[str, Any]]:
        return list(self._history)


# Global singleton transport for in-process simulated streaming
_global_transport = EventTransport()


def get_global_transport() -> EventTransport:
    return _global_transport
