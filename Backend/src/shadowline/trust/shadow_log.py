"""Shadow log recording all predictions for retrospective scoring."""

from datetime import datetime, timezone
import logging
from typing import Dict, List, Optional
from shadowline.domain.prediction import Prediction

logger = logging.getLogger("shadowline.trust.shadow_log")


class ShadowLog:
    """Stores all predictions for retrospective scoring and auditing."""

    def __init__(self):
        self._predictions: Dict[str, Prediction] = {}

    def log_prediction(self, prediction: Prediction) -> None:
        self._predictions[prediction.id] = prediction

    def log_batch(self, predictions: List[Prediction]) -> None:
        for p in predictions:
            self._predictions[p.id] = p

    def get_unscored_predictions(self, now: Optional[datetime] = None) -> List[Prediction]:
        current_time = now or datetime.now(timezone.utc)
        unscored = []
        for p in self._predictions.values():
            if not p.is_scored and p.expected_impact_time:
                # Horizon has elapsed
                if current_time >= p.expected_impact_time:
                    unscored.append(p)
        return unscored

    def all_predictions(self) -> List[Prediction]:
        return list(self._predictions.values())

    def get(self, prediction_id: str) -> Optional[Prediction]:
        return self._predictions.get(prediction_id)
