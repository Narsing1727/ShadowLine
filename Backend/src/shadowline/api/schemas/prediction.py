"""Prediction API schemas."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from shadowline.api.schemas.alert import ExplanationSchema


class PredictionItemResponse(BaseModel):
    id: str
    prediction_type: str
    subject_id: str
    predicted_at: str
    horizon_hours: float
    probability: float
    calibrated_probability: float
    confidence_tier: str
    expected_impact_time: Optional[str]
    predicted_state: Optional[str]
    explanation: Optional[ExplanationSchema]
    is_scored: bool
    actual_outcome: Optional[bool]


class BottleneckForecastResponse(BaseModel):
    timestamp: str
    horizons_hours: List[float]
    top_bottlenecks: Dict[str, str]
    station_probabilities: Dict[str, Dict[str, float]]
    predictions: List[PredictionItemResponse]
