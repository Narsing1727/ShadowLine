"""Coverage tier classifier based on observed signal completeness."""

from typing import Dict, List
from shadowline.domain.enums import ConfidenceTier
from shadowline.twin.snapshot import TwinSnapshot


class CoverageClassifier:
    """Classifies station instrumentation level into MEASURED, INFERRED, or DARK."""

    @staticmethod
    def classify(station_id: str, snapshot: TwinSnapshot) -> ConfidenceTier:
        s_snap = snapshot.stations.get(station_id)
        if not s_snap:
            return ConfidenceTier.DARK

        # Explicit config tier takes precedence
        if s_snap.confidence_tier in ConfidenceTier.__members__:
            return ConfidenceTier(s_snap.confidence_tier)

        if s_snap.last_cycle_time is not None and s_snap.total_units_processed > 0:
            return ConfidenceTier.MEASURED
        elif s_snap.total_units_processed > 0:
            return ConfidenceTier.INFERRED
        else:
            return ConfidenceTier.DARK
