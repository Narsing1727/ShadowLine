"""Overall Equipment Effectiveness (OEE) calculation."""

from dataclasses import dataclass
from shadowline.twin.snapshot import TwinSnapshot


@dataclass
class OEEResult:
    availability: float
    performance: float
    quality: float
    oee: float
    target_jph: float
    actual_jph: float


class OEECalculator:
    """Computes line-level Availability, Performance, Quality, and OEE."""

    @staticmethod
    def calculate(
        snapshot: TwinSnapshot,
        operating_hours: float = 8.0,
        target_jph: float = 62.0,
    ) -> OEEResult:
        if not snapshot.stations:
            return OEEResult(1.0, 1.0, 1.0, 1.0, target_jph, target_jph)

        # 1. Availability: (Planned Time - Down Time) / Planned Time
        total_down = sum(s.down_period_seconds for s in snapshot.stations.values())
        mean_down_hours = (total_down / len(snapshot.stations)) / 3600.0
        availability = max(0.0, min(1.0, (operating_hours - mean_down_hours) / max(0.1, operating_hours)))

        # 2. Performance: Actual Units / Ideal Units
        total_units = max((s.total_units_processed for s in snapshot.stations.values()), default=0)
        ideal_units = target_jph * operating_hours
        actual_jph = total_units / max(0.1, operating_hours)
        performance = max(0.0, min(1.0, actual_jph / max(1.0, target_jph)))

        # 3. Quality: Good Units / Total Units
        defect_units = len([u for u in snapshot.in_flight_units.values() if u.defect_codes])
        good_units = max(0, total_units - defect_units)
        quality = (good_units / total_units) if total_units > 0 else 0.98

        oee = availability * performance * quality

        return OEEResult(
            availability=round(availability, 3),
            performance=round(performance, 3),
            quality=round(quality, 3),
            oee=round(oee, 3),
            target_jph=target_jph,
            actual_jph=round(actual_jph, 1),
        )
