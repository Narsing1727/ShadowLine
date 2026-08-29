"""Bottleneck Prediction Head aggregating Active Period Method and Monte Carlo forecasts."""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from shadowline.domain.enums import ConfidenceTier, PredictionType
from shadowline.domain.evidence import EvidenceItem, Explanation
from shadowline.domain.prediction import Prediction
from shadowline.prediction.base import PredictionHead
from shadowline.prediction.bottleneck.active_period import ActivePeriodCalculator
from shadowline.prediction.bottleneck.horizon_forecast import MultiHorizonForecaster
from shadowline.prediction.bottleneck.monte_carlo import MonteCarloForecaster
from shadowline.prediction.bottleneck.shifting_detector import ShiftingBottleneckDetector
from shadowline.twin.snapshot import TwinSnapshot


class BottleneckPredictionHead(PredictionHead):
    """Integrates APM, shifting detection, and Monte Carlo forward runs."""

    def __init__(self, num_mc_runs: int = 50, takt_time: float = 58.0):
        self._name = "bottleneck_head"
        self.mc_forecaster = MonteCarloForecaster(num_runs=num_mc_runs, takt_time=takt_time)
        self.multi_horizon = MultiHorizonForecaster(forecaster=self.mc_forecaster, horizons=[1.0, 2.0, 4.0])
        self.shifting_detector = ShiftingBottleneckDetector()

    @property
    def name(self) -> str:
        return self._name

    def predict(self, snapshot: TwinSnapshot, **kwargs) -> List[Prediction]:
        predictions: List[Prediction] = []

        # 1. Compute Active Period Method
        apm_results = ActivePeriodCalculator.calculate(snapshot)

        # 2. Run multi-horizon Monte Carlo forecast
        horizon_forecast = self.multi_horizon.forecast(snapshot)

        # Track shifting history
        current_b = next((s_id for s_id, res in apm_results.items() if res.is_current_bottleneck), None)
        if current_b:
            self.shifting_detector.record_bottleneck(current_b)

        shifting_info = self.shifting_detector.detect()

        now_utc = datetime.now(timezone.utc)

        # 3. Formulate Predictions for each horizon
        for horizon in horizon_forecast.horizons_hours:
            probs = horizon_forecast.per_horizon_probabilities.get(horizon, {})
            for station_id, prob in probs.items():
                if prob < 0.15:  # filter noise
                    continue

                s_snap = snapshot.stations.get(station_id)
                tier_str = s_snap.confidence_tier if s_snap else "MEASURED"
                try:
                    conf_tier = ConfidenceTier(tier_str)
                except ValueError:
                    conf_tier = ConfidenceTier.MEASURED

                apm_res = apm_results.get(station_id)
                act_pct = apm_res.active_percentage if apm_res else 0.0
                blk_pct = apm_res.blocked_percentage if apm_res else 0.0

                evidence = [
                    EvidenceItem(
                        metric_name="monte_carlo_probability",
                        observed_value=round(prob, 3),
                        threshold_value=0.50,
                        unit="prob",
                        description=f"Monte Carlo simulation predicted {station_id} as bottleneck in {prob * 100:.1f}% of runs over {horizon}h horizon.",
                    ),
                    EvidenceItem(
                        metric_name="active_period_ratio",
                        observed_value=round(act_pct, 3),
                        threshold_value=0.75,
                        unit="ratio",
                        description=f"Observed working active ratio is {act_pct * 100:.1f}%.",
                    ),
                ]

                explanation = Explanation(
                    summary=f"Station {station_id} ({s_snap.name if s_snap else ''}) forecast to become bottleneck with {prob * 100:.1f}% probability within {horizon} hours.",
                    key_factors=[
                        f"Nominal cycle time: {s_snap.nominal_cycle_time if s_snap else 0}s vs line takt {self.mc_forecaster.takt_time}s",
                        f"Active time ratio: {act_pct * 100:.1f}%",
                        f"Downstream blocking ratio: {blk_pct * 100:.1f}%",
                    ],
                    evidence_items=evidence,
                    recommended_actions=[
                        f"Check buffer infeed and outfeed capacities around {station_id}.",
                        f"Verify tooling calibration and cycle time stability on {station_id}.",
                    ],
                )

                pred = Prediction.create(
                    prediction_type=PredictionType.BOTTLENECK,
                    subject_id=station_id,
                    horizon_hours=horizon,
                    probability=prob,
                    calibrated_probability=prob,  # Will be refined by calibration layer
                    confidence_tier=conf_tier,
                    expected_impact_time=now_utc + timedelta(hours=horizon),
                    predicted_state="ACTIVE",
                    predicted_metric_value=prob,
                    explanation=explanation,
                    metadata={
                        "station_name": s_snap.name if s_snap else station_id,
                        "zone": s_snap.zone if s_snap else "UNKNOWN",
                        "is_shifting": shifting_info.is_shifting,
                        "dominant_station_id": shifting_info.dominant_station_id,
                    },
                )
                predictions.append(pred)

        return predictions
