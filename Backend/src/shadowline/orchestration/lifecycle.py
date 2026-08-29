"""Service lifecycle manager."""

import asyncio
import logging
from typing import Optional

from shadowline.calibration.isotonic import IsotonicCalibrator
from shadowline.config.line_loader import LineLoader
from shadowline.config.mode import ModeManager
from shadowline.config.settings import ShadowLineSettings
from shadowline.decision.alarm_budget import AlarmBudgetManager
from shadowline.decision.ranker import DecisionEngine
from shadowline.decision.suppression import AlertSuppressionEngine
from shadowline.domain.enums import Mode
from shadowline.ingestion.adapters.simulated import SimulatedIngestionAdapter
from shadowline.orchestration.prediction_cycle import PredictionCycleRunner
from shadowline.orchestration.scheduler import CycleScheduler
from shadowline.persistence.engine import init_db
from shadowline.prediction.bottleneck.aggregator import BottleneckPredictionHead
from shadowline.prediction.registry import PredictionRegistry
from shadowline.telemetry.metrics import MetricsCollector
from shadowline.trust.promotion_gate import PromotionGate
from shadowline.trust.shadow_log import ShadowLog
from shadowline.twin.state_store import StateStore

logger = logging.getLogger("shadowline.orchestration.lifecycle")


class ServiceContainer:
    """Dependency container holding all singleton services for the ShadowLine application."""

    def __init__(self, settings: Optional[ShadowLineSettings] = None):
        self.settings = settings or ShadowLineSettings()
        init_db(self.settings.db_url)

        self.mode_manager = ModeManager(
            initial_mode=Mode.LIVE if self.settings.mode.upper() == "LIVE" else Mode.SHADOW
        )
        self.topology = LineLoader.load_from_yaml(self.settings.line_config)
        self.state_store = StateStore(self.topology)
        self.metrics_collector = MetricsCollector()

        # Ingestion
        self.ingestion_adapter = SimulatedIngestionAdapter()

        # Prediction
        self.prediction_registry = PredictionRegistry()
        self.bottleneck_head = BottleneckPredictionHead(
            num_mc_runs=self.settings.monte_carlo_runs,
            takt_time=self.topology.takt_time_seconds,
        )
        self.prediction_registry.register(self.bottleneck_head)

        # Calibration
        self.calibrator = IsotonicCalibrator()

        # Decision
        self.alarm_budget = AlarmBudgetManager(
            max_alerts_per_hour=self.settings.alarm_budget_per_operator_per_hour
        )
        self.suppression_engine = AlertSuppressionEngine()
        self.decision_engine = DecisionEngine(self.alarm_budget, self.suppression_engine)

        # Trust
        self.shadow_log = ShadowLog()
        self.promotion_gate = PromotionGate()
        self._load_persisted_predictions()

        # Runner & Scheduler
        self.cycle_runner = PredictionCycleRunner(
            state_store=self.state_store,
            prediction_registry=self.prediction_registry,
            calibrator=self.calibrator,
            decision_engine=self.decision_engine,
            shadow_log=self.shadow_log,
            promotion_gate=self.promotion_gate,
            mode_manager=self.mode_manager,
            metrics_collector=self.metrics_collector,
        )
        self.scheduler = CycleScheduler(
            runner=self.cycle_runner,
            interval_seconds=self.settings.fork_interval_seconds,
        )
        self._ingest_task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        logger.info("Starting ShadowLine service container...")
        await self.ingestion_adapter.start()
        self._ingest_task = asyncio.create_task(self._ingest_loop())
        await self.scheduler.start()
        logger.info("ShadowLine service container running.")

    async def stop(self) -> None:
        logger.info("Stopping ShadowLine service container...")
        await self.scheduler.stop()
        if self._ingest_task:
            self._ingest_task.cancel()
        await self.ingestion_adapter.stop()
        logger.info("ShadowLine service container stopped.")

    async def _ingest_loop(self) -> None:
        async for event in self.ingestion_adapter.stream_events():
            self.state_store.apply_event(event)

    def _load_persisted_predictions(self) -> None:
        try:
            from sqlalchemy.orm import sessionmaker
            from shadowline.domain.enums import ConfidenceTier, PredictionType
            from shadowline.domain.prediction import Prediction
            from shadowline.persistence.engine import get_db_engine
            from shadowline.persistence.models import PredictionModel

            engine = get_db_engine(self.settings.db_url)
            Session = sessionmaker(bind=engine)
            session = Session()

            models = session.query(PredictionModel).limit(500).all()
            for m in models:
                try:
                    p_type = PredictionType(m.prediction_type)
                    tier = ConfidenceTier(m.confidence_tier) if m.confidence_tier in ConfidenceTier.__members__ else ConfidenceTier.MEASURED
                    pred = Prediction(
                        id=m.id,
                        prediction_type=p_type,
                        subject_id=m.subject_id,
                        predicted_at=m.predicted_at,
                        horizon_hours=m.horizon_hours,
                        probability=m.probability,
                        calibrated_probability=m.calibrated_probability,
                        confidence_tier=tier,
                        expected_impact_time=m.expected_impact_time,
                        predicted_state=m.predicted_state,
                        predicted_metric_value=m.predicted_metric_value,
                        is_scored=m.is_scored,
                        actual_outcome=m.actual_outcome,
                        scored_at=m.scored_at,
                    )
                    self.shadow_log.log_prediction(pred)
                except Exception:
                    pass
            session.close()
        except Exception as e:
            logger.warning("Could not load persisted predictions: %s", e)
