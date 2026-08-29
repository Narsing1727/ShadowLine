"""Outcome matcher comparing predictions to ground-truth line state."""

from datetime import datetime, timezone
import logging
from typing import Dict, List, Optional
from shadowline.domain.enums import PredictionType, StationState
from shadowline.domain.prediction import Prediction
from shadowline.twin.snapshot import TwinSnapshot

logger = logging.getLogger("shadowline.trust.outcome_matcher")


class OutcomeMatcher:
    """Compares elapsed predictions against actual observed digital twin states."""

    @staticmethod
    def match_outcomes(
        unscored_predictions: List[Prediction],
        current_snapshot: TwinSnapshot,
        now: Optional[datetime] = None,
    ) -> List[Prediction]:
        scored = []
        scored_at = now or datetime.now(timezone.utc)

        for pred in unscored_predictions:
            s_id = pred.subject_id
            s_snap = current_snapshot.stations.get(s_id)
            if not s_snap:
                continue

            actual = False
            if pred.prediction_type == PredictionType.BOTTLENECK:
                # Actual bottleneck if station has highest active ratio or was down/blocked
                total = s_snap.active_period_seconds + s_snap.blocked_period_seconds + s_snap.starved_period_seconds
                if total > 0:
                    act_ratio = s_snap.active_period_seconds / total
                    actual = act_ratio >= 0.60 or s_snap.current_state in {"ACTIVE", "DOWN"}
                else:
                    actual = s_snap.current_state == "ACTIVE"

            elif pred.prediction_type == PredictionType.DEFECT_PROPAGATION:
                # Actual if defects were detected associated with this station
                actual = any(s_id in u.defect_codes for u in current_snapshot.in_flight_units.values())

            elif pred.prediction_type == PredictionType.SOFT_SENSOR:
                actual = s_snap.total_units_processed > 0

            pred.is_scored = True
            pred.actual_outcome = actual
            pred.scored_at = scored_at
            scored.append(pred)

        return scored
