"""Promotion gate evaluating readiness to transition from SHADOW to LIVE mode."""

from dataclasses import dataclass
from typing import Any, Dict, List
from shadowline.trust.scorecard import TrustScorecard


@dataclass
class PromotionGateResult:
    is_eligible_for_live: bool
    current_mode: str
    sample_size_passed: bool
    precision_passed: bool
    false_alarm_passed: bool
    lead_time_passed: bool
    brier_score_passed: bool
    reasons: List[str]
    scorecard_summary: Dict[str, Any]


class PromotionGate:
    """Evaluates whether the digital twin's track record satisfies promotion criteria."""

    def __init__(
        self,
        min_precision: float = 0.80,
        max_false_alarm_rate: float = 0.15,
        min_sample_size: int = 50,
        min_mean_lead_time_minutes: float = 15.0,
        max_brier_score: float = 0.20,
    ):
        self.min_precision = min_precision
        self.max_false_alarm_rate = max_false_alarm_rate
        self.min_sample_size = min_sample_size
        self.min_mean_lead_time_minutes = min_mean_lead_time_minutes
        self.max_brier_score = max_brier_score

    def evaluate(self, scorecard: TrustScorecard, current_mode: str = "SHADOW") -> PromotionGateResult:
        sample_passed = scorecard.scored_predictions >= self.min_sample_size
        precision_passed = scorecard.precision >= self.min_precision
        fa_passed = scorecard.false_alarm_rate <= self.max_false_alarm_rate
        lead_passed = scorecard.mean_lead_time_minutes >= self.min_mean_lead_time_minutes
        brier_passed = scorecard.reliability_data.brier_score <= self.max_brier_score

        reasons = []
        if not sample_passed:
            reasons.append(f"Insufficient sample size: {scorecard.scored_predictions}/{self.min_sample_size} predictions scored.")
        if not precision_passed:
            reasons.append(f"Precision below threshold: {scorecard.precision:.2f} < {self.min_precision:.2f}")
        if not fa_passed:
            reasons.append(f"False alarm rate exceeds limit: {scorecard.false_alarm_rate:.2f} > {self.max_false_alarm_rate:.2f}")
        if not lead_passed:
            reasons.append(f"Lead time too short: {scorecard.mean_lead_time_minutes:.1f}m < {self.min_mean_lead_time_minutes:.1f}m")
        if not brier_passed:
            reasons.append(f"Brier score above target: {scorecard.reliability_data.brier_score:.3f} > {self.max_brier_score:.3f}")

        eligible = sample_passed and precision_passed and fa_passed and lead_passed and brier_passed

        if eligible and not reasons:
            reasons.append("All promotion gate criteria successfully satisfied. System is certified for LIVE mode.")

        return PromotionGateResult(
            is_eligible_for_live=eligible,
            current_mode=current_mode,
            sample_size_passed=sample_passed,
            precision_passed=precision_passed,
            false_alarm_passed=fa_passed,
            lead_time_passed=lead_passed,
            brier_score_passed=brier_passed,
            reasons=reasons,
            scorecard_summary={
                "scored_predictions": scorecard.scored_predictions,
                "precision": scorecard.precision,
                "false_alarm_rate": scorecard.false_alarm_rate,
                "mean_lead_time_minutes": scorecard.mean_lead_time_minutes,
                "brier_score": scorecard.reliability_data.brier_score,
            },
        )
