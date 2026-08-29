"""Unit genealogy tracking in digital twin."""

from datetime import datetime, timezone
import logging
from typing import Dict, List, Optional

from shadowline.domain.enums import Variant
from shadowline.domain.genealogy import GenealogyRecord, GenealogyStep

logger = logging.getLogger("shadowline.twin.genealogy")


class GenealogyTracker:
    """Maintains comprehensive genealogy traces for all VINs entering the line."""

    def __init__(self):
        self._records: Dict[str, GenealogyRecord] = {}

    def get_or_create(self, vin: str, variant: Variant = Variant.SUV_A, entered_at: Optional[datetime] = None) -> GenealogyRecord:
        if vin not in self._records:
            self._records[vin] = GenealogyRecord(
                vin=vin,
                variant=variant,
                created_at=entered_at or datetime.now(timezone.utc),
            )
        return self._records[vin]

    def record_entry(self, vin: str, station_id: str, station_name: str, entered_at: datetime) -> None:
        rec = self.get_or_create(vin, entered_at=entered_at)
        step = GenealogyStep(
            station_id=station_id,
            station_name=station_name,
            entered_at=entered_at,
        )
        rec.add_step(step)

    def record_exit(self, vin: str, station_id: str, exited_at: datetime, dwell_seconds: Optional[float] = None) -> None:
        if vin not in self._records:
            return
        rec = self._records[vin]
        for step in reversed(rec.steps):
            if step.station_id == station_id and step.exited_at is None:
                step.exited_at = exited_at
                step.dwell_seconds = dwell_seconds or (exited_at - step.entered_at).total_seconds()
                break

    def record_defect(
        self,
        vin: str,
        defect_code: str,
        detecting_station_id: str,
        detected_at: datetime,
        suspected_causing_station_id: Optional[str] = None,
    ) -> None:
        rec = self.get_or_create(vin, entered_at=detected_at)
        rec.record_defect(defect_code, detecting_station_id, detected_at, suspected_causing_station_id)

    def get_genealogy(self, vin: str) -> Optional[GenealogyRecord]:
        return self._records.get(vin)

    def all_vins(self) -> List[str]:
        return list(self._records.keys())
