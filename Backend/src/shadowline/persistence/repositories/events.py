"""Event repository."""

import json
from typing import List, Optional
from sqlalchemy.orm import Session
from shadowline.domain.events import CanonicalEvent
from shadowline.persistence.models import EventModel


class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, event: CanonicalEvent) -> None:
        model = EventModel(
            event_id=event.event_id,
            event_type=event.event_type.value,
            occurred_at=event.occurred_at,
            ingested_at=event.ingested_at,
            station_id=event.station_id,
            zone=event.zone.value if event.zone else None,
            confidence_tier=event.confidence_tier.value,
            source=event.source,
            payload_json=json.dumps(event.payload),
        )
        self.session.merge(model)
        self.session.commit()

    def save_batch(self, events: List[CanonicalEvent]) -> None:
        for event in events:
            model = EventModel(
                event_id=event.event_id,
                event_type=event.event_type.value,
                occurred_at=event.occurred_at,
                ingested_at=event.ingested_at,
                station_id=event.station_id,
                zone=event.zone.value if event.zone else None,
                confidence_tier=event.confidence_tier.value,
                source=event.source,
                payload_json=json.dumps(event.payload),
            )
            self.session.merge(model)
        self.session.commit()

    def list_recent(self, limit: int = 100) -> List[EventModel]:
        return self.session.query(EventModel).order_by(EventModel.occurred_at.desc()).limit(limit).all()
