"""Alert ranking and conversion engine."""

from datetime import datetime, timezone
import logging
from typing import List, Tuple
from shadowline.domain.alert import Alert
from shadowline.domain.enums import AlertSeverity, ConfidenceTier, PredictionType
from shadowline.domain.prediction import Prediction
from shadowline.decision.alarm_budget import AlarmBudgetManager
from shadowline.decision.explanation import ExplanationBuilder
from shadowline.decision.recommendation import RecommendationEngine
from shadowline.decision.suppression import AlertSuppressionEngine

logger = logging.getLogger("shadowline.decision.ranker")


class DecisionEngine:
    """Ranks predictions, enforces alarm budget and suppression, and produces surfaceable Alerts."""

    def __init__(
        self,
        alarm_budget: AlarmBudgetManager,
        suppression_engine: AlertSuppressionEngine,
    ):
        self.alarm_budget = alarm_budget
        self.suppression_engine = suppression_engine

    def evaluate_predictions(
        self,
        predictions: List[Prediction],
        now: datetime | None = None,
    ) -> Tuple[List[Alert], List[Prediction]]:
        """Separates predictions into surfaced Alerts and Suppressed Predictions."""
        current_time = now or datetime.now(timezone.utc)

        # 1. Rank predictions by calibrated probability descending
        ranked_preds = sorted(
            predictions,
            key=lambda p: (
                p.calibrated_probability,
                -p.horizon_hours,  # Closer horizon first
            ),
            reverse=True,
        )

        surfaced_alerts: List[Alert] = []
        suppressed_preds: List[Prediction] = []

        for pred in ranked_preds:
            # Determine severity
            prob = pred.calibrated_probability
            if prob >= 0.85:
                severity = AlertSeverity.CRITICAL
            elif prob >= 0.70:
                severity = AlertSeverity.HIGH
            elif prob >= 0.50:
                severity = AlertSeverity.MEDIUM
            else:
                severity = AlertSeverity.LOW

            # Check chatter suppression
            alert_type_str = pred.prediction_type.value
            if self.suppression_engine.is_suppressed(pred.subject_id, alert_type_str, now=current_time):
                suppressed_preds.append(pred)
                continue

            # Check alarm budget
            if not self.alarm_budget.can_surface_alert(now=current_time):
                suppressed_preds.append(pred)
                continue

            # Surface as Alert
            self.alarm_budget.record_surfaced_alert(now=current_time)
            self.suppression_engine.record_alert(pred.subject_id, alert_type_str, now=current_time)

            explanation = ExplanationBuilder.build_from_prediction(pred)
            recs = RecommendationEngine.generate_recommendations(pred)

            alert = Alert.create(
                station_id=pred.subject_id,
                severity=severity,
                confidence=pred.calibrated_probability,
                confidence_tier=pred.confidence_tier,
                title=f"{pred.prediction_type.value.replace('_', ' ').title()} Alert: {pred.subject_id}",
                message=explanation.summary,
                prediction_id=pred.id,
                explanation=explanation,
                recommended_actions=recs,
                metadata=pred.metadata,
            )
            surfaced_alerts.append(alert)

        return surfaced_alerts, suppressed_preds
