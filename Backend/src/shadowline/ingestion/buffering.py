"""Ingestion event buffer with backpressure and rate tracking."""

import asyncio
from datetime import datetime, timezone
from typing import List, Optional
from shadowline.domain.events import CanonicalEvent


class EventBuffer:
    """Async FIFO buffer for incoming CanonicalEvents."""

    def __init__(self, maxsize: int = 10000):
        self.queue: asyncio.Queue[CanonicalEvent] = asyncio.Queue(maxsize=maxsize)
        self.total_received = 0
        self.total_dropped = 0
        self.last_received_at: Optional[datetime] = None

    async def put(self, event: CanonicalEvent) -> bool:
        self.total_received += 1
        self.last_received_at = datetime.now(timezone.utc)
        try:
            self.queue.put_nowait(event)
            return True
        except asyncio.QueueFull:
            self.total_dropped += 1
            # Evict oldest item to prevent memory exhaustion
            try:
                self.queue.get_nowait()
                self.queue.put_nowait(event)
                return True
            except Exception:
                return False

    async def get(self) -> CanonicalEvent:
        return await self.queue.get()

    def get_batch(self, max_items: int = 100) -> List[CanonicalEvent]:
        items: List[CanonicalEvent] = []
        while len(items) < max_items and not self.queue.empty():
            try:
                items.append(self.queue.get_nowait())
            except asyncio.QueueEmpty:
                break
        return items

    @property
    def size(self) -> int:
        return self.queue.qsize()
