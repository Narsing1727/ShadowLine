"""Canonical wire and internal event schema."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid

from shadowline.domain.enums import ConfidenceTier, EventType, Zone


@dataclass
class CanonicalEvent:
    event_id: str
    event_type: EventType
    occurred_at: datetime
    ingested_at: datetime
    station_id: Optional[str] = None
    zone: Optional[Zone] = None
    confidence_tier: ConfidenceTier = ConfidenceTier.MEASURED
    source: str = "simulated"
    payload: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        event_type: EventType,
        occurred_at: datetime,
        station_id: Optional[str] = None,
        zone: Optional[Zone] = None,
        confidence_tier: ConfidenceTier = ConfidenceTier.MEASURED,
        source: str = "simulated",
        payload: Optional[Dict[str, Any]] = None,
        event_id: Optional[str] = None,
    ) -> "CanonicalEvent":
        now = datetime.now(timezone.utc)
        return cls(
            event_id=event_id or str(uuid.uuid4()),
            event_type=event_type,
            occurred_at=occurred_at,
            ingested_at=now,
            station_id=station_id,
            zone=zone,
            confidence_tier=confidence_tier,
            source=source,
            payload=payload or {},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "occurred_at": self.occurred_at.isoformat(),
            "ingested_at": self.ingested_at.isoformat(),
            "station_id": self.station_id,
            "zone": self.zone.value if self.zone else None,
            "confidence_tier": self.confidence_tier.value,
            "source": self.source,
            "payload": self.payload,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CanonicalEvent":
        occurred_at = data.get("occurred_at")
        if isinstance(occurred_at, str):
            occurred_at = datetime.fromisoformat(occurred_at)
        ingested_at = data.get("ingested_at")
        if isinstance(ingested_at, str):
            ingested_at = datetime.fromisoformat(ingested_at)
        elif ingested_at is None:
            ingested_at = datetime.now(timezone.utc)

        zone_val = data.get("zone")
        zone = Zone(zone_val) if zone_val else None

        tier_val = data.get("confidence_tier", "MEASURED")
        confidence_tier = ConfidenceTier(tier_val) if tier_val else ConfidenceTier.MEASURED

        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=EventType(data["event_type"]),
            occurred_at=occurred_at,
            ingested_at=ingested_at,
            station_id=data.get("station_id"),
            zone=zone,
            confidence_tier=confidence_tier,
            source=data.get("source", "unknown"),
            payload=data.get("payload", {}),
        )
