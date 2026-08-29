"""Simulated plant event stream generator."""

from datetime import datetime, timezone
import uuid
from typing import Any, Callable, Dict, List, Optional
from sim_plant.clock import SimClock
from sim_plant.emit.sensor_gaps import SensorGapFilter


class SimEventStream:
    def __init__(self, clock: SimClock, sink: Optional[Callable[[Dict[str, Any]], None]] = None):
        self.clock = clock
        self.sink = sink
        self.emitted_events: List[Dict[str, Any]] = []

    def emit(self, event_type: str, sim_time_seconds: float, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        filtered_payload = SensorGapFilter.filter_event(event_type, payload)
        if filtered_payload is None:
            return None

        occurred_at = self.clock.sim_to_datetime(sim_time_seconds)
        event_dict = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "occurred_at": occurred_at.isoformat(),
            "station_id": filtered_payload.get("station_id"),
            "zone": filtered_payload.get("zone"),
            "confidence_tier": filtered_payload.get("confidence_tier", "MEASURED"),
            "source": "simulated",
            "payload": filtered_payload,
        }

        self.emitted_events.append(event_dict)
        if self.sink:
            self.sink(event_dict)
        return event_dict
