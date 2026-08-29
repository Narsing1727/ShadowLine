"""Prediction layer package."""

from shadowline.prediction.base import PredictionHead
from shadowline.prediction.bottleneck.aggregator import BottleneckPredictionHead
from shadowline.prediction.registry import PredictionRegistry

__all__ = ["BottleneckPredictionHead", "PredictionHead", "PredictionRegistry"]
