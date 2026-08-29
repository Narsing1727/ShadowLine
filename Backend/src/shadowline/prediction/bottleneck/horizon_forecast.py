"""Horizon multi-step bottleneck forecast aggregation."""

from dataclasses import dataclass
from typing import Dict, List
from shadowline.prediction.bottleneck.monte_carlo import MonteCarloForecaster, MonteCarloRunSummary
from shadowline.twin.snapshot import TwinSnapshot


@dataclass
class HorizonForecast:
    horizons_hours: List[float]
    per_horizon_probabilities: Dict[float, Dict[str, float]]
    top_predicted_bottlenecks: Dict[float, str]


class MultiHorizonForecaster:
    """Computes bottleneck probabilities at multiple horizons (e.g. 1h, 2h, 4h)."""

    def __init__(self, forecaster: MonteCarloForecaster, horizons: List[float] | None = None):
        self.forecaster = forecaster
        self.horizons = horizons or [1.0, 2.0, 4.0]

    def forecast(self, snapshot: TwinSnapshot) -> HorizonForecast:
        per_horizon_probs: Dict[float, Dict[str, float]] = {}
        top_bottlenecks: Dict[float, str] = {}

        for h in self.horizons:
            summary: MonteCarloRunSummary = self.forecaster.run_forecast(snapshot, horizon_hours=h)
            per_horizon_probs[h] = summary.bottleneck_probabilities

            # Pick highest probability station
            top_s = max(summary.bottleneck_probabilities.items(), key=lambda x: x[1])[0]
            top_bottlenecks[h] = top_s

        return HorizonForecast(
            horizons_hours=self.horizons,
            per_horizon_probabilities=per_horizon_probs,
            top_predicted_bottlenecks=top_bottlenecks,
        )
