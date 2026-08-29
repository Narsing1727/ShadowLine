"""Prediction cycle executing the 60-second pipeline end-to-end."""

import asyncio
from datetime import datetime, timezone
import logging
import time
from typing import Callable, List, Optional, Tuple

from shadowline.calibration.isotonic import IsotonicCalibrator
from shadowline.config.mode import ModeManager
from shadowline.decision.ranker import DecisionEngine
from shadowline.domain.alert import Alert
from shadowline.domain.enums import Mode
from shadowline.domain.prediction import Prediction
from shadowline.prediction.registry import PredictionRegistry
from shadowline.telemetry.metrics import MetricsCollector
from shadowline.trust.outcome_matcher import OutcomeMatcher
from shadowline.trust.promotion_gate import PromotionGate, PromotionGateResult
from shadowline.trust.scorecard import ScorecardCalculator, TrustScorecard
from shadowline.trust.shadow_log import ShadowLog
from shadowline.twin.snapshot import TwinSnapshot
from shadowline.twin.state_store import StateStore

logger = logging.getLogger("shadowline.orchestration.cycle")


class PredictionCycleRunner:
    """Executes one complete forecast, calibration, decision, and trust evaluation cycle."""

    def __init__(
        self,
        state_store: StateStore,
        prediction_registry: PredictionRegistry,
        calibrator: IsotonicCalibrator,
        decision_engine: DecisionEngine,
        shadow_log: ShadowLog,
        promotion_gate: PromotionGate,
        mode_manager: ModeManager,
        metrics_collector: MetricsCollector,
        on_alerts_surfaced: Optional[Callable[[List[Alert]], None]] = None,
        on_state_updated: Optional[Callable[[TwinSnapshot], None]] = None,
    ):
        self.state_store = state_store
        self.prediction_registry = prediction_registry
        self.calibrator = calibrator
        self.decision_engine = decision_engine
        self.shadow_log = shadow_log
        self.promotion_gate = promotion_gate
        self.mode_manager = mode_manager
        self.metrics_collector = metrics_collector
        self.on_alerts_surfaced = on_alerts_surfaced
        self.on_state_updated = on_state_updated

        self.latest_scorecard: Optional[TrustScorecard] = None
        self.latest_promotion_result: Optional[PromotionGateResult] = None
        self.active_alerts: List[Alert] = []
        self.suppressed_predictions: List[Prediction] = []

    def run_cycle(self) -> Tuple[List[Prediction], List[Alert], List[Prediction]]:
        t_start = time.perf_counter()
        now_utc = datetime.now(timezone.utc)

        # 1. Snapshot live twin
        snapshot = self.state_store.snapshot()
        if self.on_state_updated:
            self.on_state_updated(snapshot)

        # 2. Run all registered prediction heads
        all_raw_predictions: List[Prediction] = []
        for head in self.prediction_registry.all_heads():
            try:
                preds = head.predict(snapshot)
                all_raw_predictions.extend(preds)
            except Exception as e:
                logger.error("Error running prediction head %s: %s", head.name, e)

        # 3. Calibrate probabilities
        for pred in all_raw_predictions:
            pred.calibrated_probability = self.calibrator.calibrate(pred.probability)

        # 4. Log all predictions into ShadowLog
        self.shadow_log.log_batch(all_raw_predictions)

        # 5. Outcome matching on expired predictions
        unscored = self.shadow_log.get_unscored_predictions(now=now_utc)
        if unscored:
            OutcomeMatcher.match_outcomes(unscored, snapshot, now=now_utc)

        # 6. Compute rolling Trust Scorecard & Evaluate Promotion Gate
        all_logged = self.shadow_log.all_predictions()
        self.latest_scorecard = ScorecardCalculator.calculate(all_logged)
        self.latest_promotion_result = self.promotion_gate.evaluate(
            self.latest_scorecard, current_mode=self.mode_manager.current_mode.value
        )

        # 7. Decision layer (Rank, Budget, Suppress)
        surfaced_alerts: List[Alert] = []
        suppressed: List[Prediction] = []

        if self.mode_manager.is_live:
            # LIVE MODE: Predictions that survive ranking & alarm budget become surfaceable Alerts
            surfaced_alerts, suppressed = self.decision_engine.evaluate_predictions(all_raw_predictions, now=now_utc)
            self.active_alerts = surfaced_alerts
            self.suppressed_predictions = suppressed

            if surfaced_alerts and self.on_alerts_surfaced:
                self.on_alerts_surfaced(surfaced_alerts)
        else:
            # SHADOW MODE: Compute & log, but surface zero alerts
            suppressed = all_raw_predictions
            self.active_alerts = []
            self.suppressed_predictions = suppressed

        duration = time.perf_counter() - t_start
        self.metrics_collector.record_cycle(
            duration_seconds=duration,
            predictions_count=len(all_raw_predictions),
            alerts_count=len(surfaced_alerts),
            suppressed_count=len(suppressed),
        )

        logger.info(
            "Cycle completed in %.2fs. Mode: %s | Predictions: %d | Surfaced Alerts: %d | Suppressed: %d",
            duration,
            self.mode_manager.current_mode.value,
            len(all_raw_predictions),
            len(surfaced_alerts),
            len(suppressed),
        )

        return all_raw_predictions, surfaced_alerts, suppressed
