"""Abstract base class for all prediction heads."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from shadowline.domain.prediction import Prediction
from shadowline.twin.snapshot import TwinSnapshot


class PredictionHead(ABC):
    """Abstract interface that all prediction heads implement."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def predict(self, snapshot: TwinSnapshot, **kwargs) -> List[Prediction]:
        """Consumes live twin snapshot and produces a list of Predictions."""
        pass
