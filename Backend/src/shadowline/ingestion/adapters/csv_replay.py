"""CSV historian replay ingestion adapter."""

import asyncio
import csv
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
from typing import Any, AsyncGenerator, Dict, List, Optional

from shadowline.domain.events import CanonicalEvent
from shadowline.ingestion.normalizer import EventNormalizer
from shadowline.ingestion.port import IngestionPort

logger = logging.getLogger("shadowline.ingestion.csv_replay")


class CsvReplayAdapter(IngestionPort):
    """Replays events recorded in CSV historian files."""

    def __init__(self, file_path: str, playback_speed: float = 10.0):
        self.file_path = Path(file_path)
        self.playback_speed = max(0.1, playback_speed)
        self.is_running = False
        self._events_ingested = 0
        self._events: List[Dict[str, Any]] = []

    async def start(self) -> None:
        self.is_running = True
        self._load_csv()
        logger.info("CSV replay adapter loaded %d events from %s", len(self._events), self.file_path)

    async def stop(self) -> None:
        self.is_running = False
        logger.info("CSV replay adapter stopped.")

    def _load_csv(self) -> None:
        if not self.file_path.exists():
            logger.warning("CSV replay file not found: %s", self.file_path)
            return

        with open(self.file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse JSON payload if stored as string
                payload_str = row.get("payload")
                payload = {}
                if payload_str:
                    try:
                        payload = json.loads(payload_str)
                    except Exception:
                        pass
                row["payload"] = payload
                self._events.append(row)

    async def stream_events(self) -> AsyncGenerator[CanonicalEvent, None]:
        prev_time = None
        for raw in self._events:
            if not self.is_running:
                break

            evt = EventNormalizer.normalize(raw, source="csv_replay")
            self._events_ingested += 1

            if prev_time is not None:
                delta = (evt.occurred_at - prev_time).total_seconds()
                if delta > 0:
                    sleep_time = delta / self.playback_speed
                    await asyncio.sleep(min(1.0, sleep_time))

            prev_time = evt.occurred_at
            yield evt

    async def get_health(self) -> Dict[str, Any]:
        return {
            "adapter": "csv_replay",
            "file_path": str(self.file_path),
            "is_running": self.is_running,
            "events_loaded": len(self._events),
            "events_ingested": self._events_ingested,
        }
