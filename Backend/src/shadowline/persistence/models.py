"""SQLAlchemy ORM models for ShadowLine."""

from datetime import datetime, timezone
import json
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)
from shadowline.persistence.engine import Base


class EventModel(Base):
    __tablename__ = "events"

    event_id = Column(String(64), primary_key=True, index=True)
    event_type = Column(String(64), nullable=False, index=True)
    occurred_at = Column(DateTime, nullable=False, index=True)
    ingested_at = Column(DateTime, nullable=False)
    station_id = Column(String(32), nullable=True, index=True)
    zone = Column(String(32), nullable=True)
    confidence_tier = Column(String(32), nullable=False, default="MEASURED")
    source = Column(String(32), nullable=False, default="simulated")
    payload_json = Column(Text, nullable=True)


class StationHistoryModel(Base):
    __tablename__ = "station_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String(32), nullable=False, index=True)
    state = Column(String(32), nullable=False)
    cycle_time_seconds = Column(Float, nullable=True)
    vin = Column(String(64), nullable=True)
    occurred_at = Column(DateTime, nullable=False, index=True)


class PredictionModel(Base):
    __tablename__ = "predictions"

    id = Column(String(64), primary_key=True, index=True)
    prediction_type = Column(String(64), nullable=False, index=True)
    subject_id = Column(String(32), nullable=False, index=True)
    predicted_at = Column(DateTime, nullable=False, index=True)
    horizon_hours = Column(Float, nullable=False)
    probability = Column(Float, nullable=False)
    calibrated_probability = Column(Float, nullable=False)
    confidence_tier = Column(String(32), nullable=False, default="MEASURED")
    expected_impact_time = Column(DateTime, nullable=True)
    predicted_state = Column(String(32), nullable=True)
    predicted_metric_value = Column(Float, nullable=True)
    explanation_json = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)
    is_scored = Column(Boolean, default=False, index=True)
    actual_outcome = Column(Boolean, nullable=True)
    scored_at = Column(DateTime, nullable=True)


class AlertModel(Base):
    __tablename__ = "alerts"

    id = Column(String(64), primary_key=True, index=True)
    prediction_id = Column(String(64), nullable=True)
    station_id = Column(String(32), nullable=False, index=True)
    severity = Column(String(32), nullable=False)
    status = Column(String(32), nullable=False, default="ACTIVE", index=True)
    confidence = Column(Float, nullable=False)
    confidence_tier = Column(String(32), nullable=False, default="MEASURED")
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, index=True)
    updated_at = Column(DateTime, nullable=False)
    acknowledged_at = Column(DateTime, nullable=True)
    acknowledged_by = Column(String(64), nullable=True)
    snoozed_until = Column(DateTime, nullable=True)
    dismissed_at = Column(DateTime, nullable=True)
    false_alarm = Column(Boolean, default=False)
    false_alarm_reason = Column(Text, nullable=True)
    explanation_json = Column(Text, nullable=True)
    recommendations_json = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)


class GenealogyModel(Base):
    __tablename__ = "genealogy"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vin = Column(String(64), nullable=False, index=True)
    variant = Column(String(32), nullable=False)
    station_id = Column(String(32), nullable=False, index=True)
    station_name = Column(String(128), nullable=False)
    entered_at = Column(DateTime, nullable=False)
    exited_at = Column(DateTime, nullable=True)
    dwell_seconds = Column(Float, nullable=True)
    defect_codes_json = Column(Text, nullable=True)
    measurements_json = Column(Text, nullable=True)


class ScorecardModel(Base):
    __tablename__ = "scorecards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    total_predictions = Column(Integer, nullable=False)
    scored_predictions = Column(Integer, nullable=False)
    true_positives = Column(Integer, nullable=False)
    false_positives = Column(Integer, nullable=False)
    true_negatives = Column(Integer, nullable=False)
    false_negatives = Column(Integer, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    false_alarm_rate = Column(Float, nullable=False)
    mean_lead_time_minutes = Column(Float, nullable=False)
    brier_score = Column(Float, nullable=False)
    is_live_promoted = Column(Boolean, default=False)


class DiscoverySessionModel(Base):
    __tablename__ = "discovery_sessions"

    session_id = Column(String(64), primary_key=True)
    line_name = Column(String(128), nullable=False)
    status = Column(String(32), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    events_ingested = Column(Integer, default=0)
    inferred_topology_json = Column(Text, nullable=True)
    estimated_takt_time = Column(Float, nullable=True)
