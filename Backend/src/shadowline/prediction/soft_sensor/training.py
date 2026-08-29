"""Soft-sensor training and periodic model update pipeline."""

import logging
from typing import Dict, List, Tuple
import numpy as np
from shadowline.prediction.soft_sensor.estimator import SoftSensorEstimator

logger = logging.getLogger("shadowline.prediction.soft_sensor.training")


class SoftSensorTrainer:
    """Trains regression models for soft sensor estimation from historical telemetry."""

    @staticmethod
    def train_models(
        estimator: SoftSensorEstimator,
        training_data: Dict[str, Tuple[np.ndarray, np.ndarray]],
    ) -> None:
        for s_id, (X, y) in training_data.items():
            if len(X) >= 5:
                estimator.fit_station(s_id, X, y)
                logger.info("Fitted soft sensor model for station %s (R2=%.3f)", s_id, estimator.r2_scores.get(s_id, 0.0))
