"""Predictions API router."""

from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends

from shadowline.api.deps import get_service_container
from shadowline.api.schemas.alert import EvidenceItemSchema, ExplanationSchema
from shadowline.api.schemas.prediction import BottleneckForecastResponse, PredictionItemResponse
from shadowline.domain.enums import PredictionType
from shadowline.domain.prediction import Prediction
from shadowline.orchestration.lifecycle import ServiceContainer

router = APIRouter(prefix="/api/predictions", tags=["Predictions"])


def _format_pred(p: Prediction) -> PredictionItemResponse:
    exp_schema = None
    if p.explanation:
        ev_schemas = [
            EvidenceItemSchema(
                metric_name=e.metric_name,
                observed_value=e.observed_value,
                threshold_value=e.threshold_value,
                unit=e.unit,
                description=e.description,
            )
            for e in p.explanation.evidence_items
        ]
        exp_schema = ExplanationSchema(
            summary=p.explanation.summary,
            key_factors=p.explanation.key_factors,
            evidence_items=ev_schemas,
            recommended_actions=p.explanation.recommended_actions,
        )

    return PredictionItemResponse(
        id=p.id,
        prediction_type=p.prediction_type.value,
        subject_id=p.subject_id,
        predicted_at=p.predicted_at.isoformat(),
        horizon_hours=p.horizon_hours,
        probability=round(p.probability, 3),
        calibrated_probability=round(p.calibrated_probability, 3),
        confidence_tier=p.confidence_tier.value,
        expected_impact_time=p.expected_impact_time.isoformat() if p.expected_impact_time else None,
        predicted_state=p.predicted_state,
        explanation=exp_schema,
        is_scored=p.is_scored,
        actual_outcome=p.actual_outcome,
    )


@router.get("/bottleneck", response_model=BottleneckForecastResponse)
async def get_bottleneck_forecast(container: ServiceContainer = Depends(get_service_container)):
    snapshot = container.state_store.snapshot()
    forecast = container.bottleneck_head.multi_horizon.forecast(snapshot)

    # Get recent predictions from shadow log
    recent_preds = [
        p for p in container.shadow_log.all_predictions()
        if p.prediction_type == PredictionType.BOTTLENECK
    ][-20:]

    station_probs_str_keyed = {
        f"{h}h": {s: round(prob, 3) for s, prob in probs.items() if prob > 0.05}
        for h, probs in forecast.per_horizon_probabilities.items()
    }
    top_b_str_keyed = {f"{h}h": s for h, s in forecast.top_predicted_bottlenecks.items()}

    return BottleneckForecastResponse(
        timestamp=datetime.now(timezone.utc).isoformat(),
        horizons_hours=forecast.horizons_hours,
        top_bottlenecks=top_b_str_keyed,
        station_probabilities=station_probs_str_keyed,
        predictions=[_format_pred(p) for p in recent_preds],
    )


@router.get("/bottleneck/history", response_model=List[PredictionItemResponse])
async def get_bottleneck_history(container: ServiceContainer = Depends(get_service_container)):
    preds = [
        p for p in container.shadow_log.all_predictions()
        if p.prediction_type == PredictionType.BOTTLENECK
    ][-100:]
    return [_format_pred(p) for p in preds]
