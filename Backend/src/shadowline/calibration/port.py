"""Abstract probability calibration interface."""

from abc import ABC, abstractmethod
import numpy as np


class ProbabilityCalibrator(ABC):
    """Abstract interface for probability calibration models."""

    @abstractmethod
    def fit(self, raw_probs: np.ndarray, actual_outcomes: np.ndarray) -> None:
        """Fits calibration curve against historical predictions and outcomes."""
        pass

    @abstractmethod
    def calibrate(self, raw_prob: float) -> float:
        """Maps a raw probability to an honest, calibrated probability."""
        pass
