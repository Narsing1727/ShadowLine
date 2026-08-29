"""Event normalizer converting raw adapter payloads into CanonicalEvents."""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid

from shadowline.domain.enums import ConfidenceTier, EventType, Zone
from shadowline.domain.events import CanonicalEvent


class EventNormalizer:
    """Normalizes raw event payloads from various adapters into CanonicalEvent."""

    @staticmethod
    def normalize(raw: Dict[str, Any], source: str) -> CanonicalEvent:
        event_id = raw.get("event_id") or str(uuid.uuid4())

        # Parse occurred_at
        occurred_val = raw.get("occurred_at") or raw.get("timestamp") or raw.get("time")
        if isinstance(occurred_val, str):
            try:
                occurred_at = datetime.fromisoformat(occurred_val)
            except Exception:
                occurred_at = datetime.now(timezone.utc)
        elif isinstance(occurred_val, (int, float)):
            occurred_at = datetime.fromtimestamp(occurred_val, tz=timezone.utc)
        elif isinstance(occurred_val, datetime):
            occurred_at = occurred_val
        else:
            occurred_at = datetime.now(timezone.utc)

        ingested_at = datetime.now(timezone.utc)

        # Parse EventType
        evt_type_val = raw.get("event_type") or raw.get("type") or "HEARTBEAT"
        try:
            event_type = EventType(evt_type_val)
        except ValueError:
            event_type = EventType.HEARTBEAT

        # Parse Zone
        zone_val = raw.get("zone")
        zone = Zone(zone_val) if zone_val in Zone.__members__ else None

        # Parse ConfidenceTier
        tier_val = raw.get("confidence_tier", "MEASURED")
        try:
            confidence_tier = ConfidenceTier(tier_val)
        except ValueError:
            confidence_tier = ConfidenceTier.MEASURED

        station_id = raw.get("station_id")
        payload = raw.get("payload", {})
        if not payload and isinstance(raw, dict):
            # If payload is flat at top-level
            payload = {
                k: v
                for k, v in raw.items()
                if k not in {"event_id", "event_type", "occurred_at", "ingested_at", "station_id", "zone", "confidence_tier", "source"}
            }

        return CanonicalEvent(
            event_id=event_id,
            event_type=event_type,
            occurred_at=occurred_at,
            ingested_at=ingested_at,
            station_id=station_id,
            zone=zone,
            confidence_tier=confidence_tier,
            source=source,
            payload=payload,
        )
