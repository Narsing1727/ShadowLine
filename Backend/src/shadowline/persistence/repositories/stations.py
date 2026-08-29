"""Station state history repository."""

from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from shadowline.persistence.models import StationHistoryModel


class StationRepository:
    def __init__(self, session: Session):
        self.session = session

    def record_transition(
        self,
        station_id: str,
        state: str,
        cycle_time_seconds: Optional[float] = None,
        vin: Optional[str] = None,
        occurred_at: Optional[datetime] = None,
    ) -> StationHistoryModel:
        model = StationHistoryModel(
            station_id=station_id,
            state=state,
            cycle_time_seconds=cycle_time_seconds,
            vin=vin,
            occurred_at=occurred_at or datetime.now(timezone.utc),
        )
        self.session.add(model)
        self.session.commit()
        return model

    def get_station_history(self, station_id: str, limit: int = 200) -> List[StationHistoryModel]:
        return (
            self.session.query(StationHistoryModel)
            .filter(StationHistoryModel.station_id == station_id)
            .order_by(StationHistoryModel.occurred_at.desc())
            .limit(limit)
            .all()
        )
