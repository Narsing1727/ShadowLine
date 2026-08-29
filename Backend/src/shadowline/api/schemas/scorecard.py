"""Scorecard and trust API schemas."""

from typing import Any, Dict, List
from pydantic import BaseModel


class ReliabilityCurveSchema(BaseModel):
    bin_centers: List[float]
    empirical_frequencies: List[float]
    bin_counts: List[int]
    brier_score: float
    expected_calibration_error: float


class TrustScorecardResponse(BaseModel):
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
    reliability: ReliabilityCurveSchema


class PromotionGateResponse(BaseModel):
    is_eligible_for_live: bool
    current_mode: str
    sample_size_passed: bool
    precision_passed: bool
    false_alarm_passed: bool
    lead_time_passed: bool
    brier_score_passed: bool
    reasons: List[str]
    scorecard_summary: Dict[str, Any]
