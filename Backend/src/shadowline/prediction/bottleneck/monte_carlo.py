"""Monte Carlo forward simulation engine for bottleneck forecasting."""

from dataclasses import dataclass
from typing import Dict, List
import numpy as np
from shadowline.twin.advance import AdvanceResult, TwinAdvancer
from shadowline.twin.fork import TwinForker
from shadowline.twin.snapshot import TwinSnapshot


@dataclass
class MonteCarloRunSummary:
    num_runs: int
    horizon_seconds: float
    bottleneck_counts: Dict[str, int]
    bottleneck_probabilities: Dict[str, float]
    station_mean_active_ratios: Dict[str, float]


class MonteCarloForecaster:
    """Runs N forward simulations from a twin snapshot to sample stochastic outcomes."""

    def __init__(self, num_runs: int = 50, takt_time: float = 58.0):
        self.num_runs = max(5, num_runs)
        self.takt_time = takt_time

    def run_forecast(self, snapshot: TwinSnapshot, horizon_hours: float = 4.0) -> MonteCarloRunSummary:
        horizon_sec = horizon_hours * 3600.0
        counts: Dict[str, int] = {s_id: 0 for s_id in snapshot.stations}
        active_ratios: Dict[str, List[float]] = {s_id: [] for s_id in snapshot.stations}

        for _ in range(self.num_runs):
            forked = TwinForker.fork(snapshot, takt_time=self.takt_time)
            res: AdvanceResult = TwinAdvancer.advance(forked, horizon_seconds=horizon_sec)

            b_id = res.bottleneck_station_id
            counts[b_id] = counts.get(b_id, 0) + 1

            for s_id, act_t in res.station_active_times.items():
                ratio = act_t / max(1.0, horizon_sec)
                active_ratios[s_id].append(ratio)

        probs = {s_id: counts[s_id] / float(self.num_runs) for s_id in counts}
        mean_ratios = {s_id: float(np.mean(active_ratios[s_id])) if active_ratios[s_id] else 0.0 for s_id in active_ratios}

        return MonteCarloRunSummary(
            num_runs=self.num_runs,
            horizon_seconds=horizon_sec,
            bottleneck_counts=counts,
            bottleneck_probabilities=probs,
            station_mean_active_ratios=mean_ratios,
        )
