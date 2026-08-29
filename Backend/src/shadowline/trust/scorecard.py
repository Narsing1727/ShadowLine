"""Trust scorecard calculation across scored predictions."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np
from shadowline.calibration.reliability import ReliabilityCalculator, ReliabilityCurveData
from shadowline.domain.prediction import Prediction


@dataclass
class TrustScorecard:
    total_predictions: int
    scored_predictions: int
    true_positives: int
    false_positives: int
    true_negatives: int
    false_negatives: int
    precision: float
    recall: float
    f1_score: float
    false_alarm_rate: float
    mean_lead_time_minutes: float
    reliability_data: ReliabilityCurveData
    metadata: Dict[str, float] = field(default_factory=dict)


class ScorecardCalculator:
    """Calculates precision, recall, false alarm rates, and reliability metrics."""

    @staticmethod
    def calculate(
        predictions: List[Prediction],
        classification_threshold: float = 0.50,
    ) -> TrustScorecard:
        scored = [p for p in predictions if p.is_scored and p.actual_outcome is not None]

        if not scored:
            return TrustScorecard(
                total_predictions=len(predictions),
                scored_predictions=0,
                true_positives=0,
                false_positives=0,
                true_negatives=0,
                false_negatives=0,
                precision=1.0,
                recall=1.0,
                f1_score=1.0,
                false_alarm_rate=0.0,
                mean_lead_time_minutes=30.0,
                reliability_data=ReliabilityCurveData([], [], [], 0.0, 0.0),
            )

        tp, fp, tn, fn = 0, 0, 0, 0
        lead_times = []
        probs = []
        outcomes = []

        for p in scored:
            pred_positive = p.calibrated_probability >= classification_threshold
            actual_positive = bool(p.actual_outcome)

            probs.append(p.calibrated_probability)
            outcomes.append(1 if actual_positive else 0)
            lead_times.append(p.horizon_hours * 60.0)

            if pred_positive and actual_positive:
                tp += 1
            elif pred_positive and not actual_positive:
                fp += 1
            elif not pred_positive and not actual_positive:
                tn += 1
            elif not pred_positive and actual_positive:
                fn += 1

        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 1.0
        far = fp / (tp + fp) if (tp + fp) > 0 else 0.0
        mean_lead = float(np.mean(lead_times)) if lead_times else 0.0

        rel_data = ReliabilityCalculator.calculate(probs, outcomes)

        return TrustScorecard(
            total_predictions=len(predictions),
            scored_predictions=len(scored),
            true_positives=tp,
            false_positives=fp,
            true_negatives=tn,
            false_negatives=fn,
            precision=round(precision, 3),
            recall=round(recall, 3),
            f1_score=round(f1, 3),
            false_alarm_rate=round(far, 3),
            mean_lead_time_minutes=round(mean_lead, 1),
            reliability_data=rel_data,
        )
