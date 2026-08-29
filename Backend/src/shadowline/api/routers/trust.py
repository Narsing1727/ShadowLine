"""Trust, scorecard, and promotion gate API router."""

from fastapi import APIRouter, Depends
from shadowline.api.deps import get_service_container
from shadowline.api.schemas.scorecard import (
    PromotionGateResponse,
    ReliabilityCurveSchema,
    TrustScorecardResponse,
)
from shadowline.orchestration.lifecycle import ServiceContainer
from shadowline.trust.scorecard import ScorecardCalculator

router = APIRouter(prefix="/api/trust", tags=["Trust"])


@router.get("/scorecard", response_model=TrustScorecardResponse)
async def get_trust_scorecard(container: ServiceContainer = Depends(get_service_container)):
    all_preds = container.shadow_log.all_predictions()
    sc = ScorecardCalculator.calculate(all_preds)
    rel = sc.reliability_data

    return TrustScorecardResponse(
        total_predictions=sc.total_predictions,
        scored_predictions=sc.scored_predictions,
        true_positives=sc.true_positives,
        false_positives=sc.false_positives,
        true_negatives=sc.true_negatives,
        false_negatives=sc.false_negatives,
        precision=sc.precision,
        recall=sc.recall,
        f1_score=sc.f1_score,
        false_alarm_rate=sc.false_alarm_rate,
        mean_lead_time_minutes=sc.mean_lead_time_minutes,
        reliability=ReliabilityCurveSchema(
            bin_centers=rel.bin_centers,
            empirical_frequencies=rel.empirical_frequencies,
            bin_counts=rel.bin_counts,
            brier_score=rel.brier_score,
            expected_calibration_error=rel.expected_calibration_error,
        ),
    )


@router.get("/promotion-gate", response_model=PromotionGateResponse)
async def get_promotion_gate(container: ServiceContainer = Depends(get_service_container)):
    all_preds = container.shadow_log.all_predictions()
    sc = ScorecardCalculator.calculate(all_preds)
    curr_mode = container.mode_manager.current_mode.value
    res = container.promotion_gate.evaluate(sc, current_mode=curr_mode)

    return PromotionGateResponse(
        is_eligible_for_live=res.is_eligible_for_live,
        current_mode=res.current_mode,
        sample_size_passed=res.sample_size_passed,
        precision_passed=res.precision_passed,
        false_alarm_passed=res.false_alarm_passed,
        lead_time_passed=res.lead_time_passed,
        brier_score_passed=res.brier_score_passed,
        reasons=res.reasons,
        scorecard_summary=res.scorecard_summary,
    )
