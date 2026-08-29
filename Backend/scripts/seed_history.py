"""Seed database with realistic historical line telemetry, predictions, and scorecards."""

from datetime import datetime, timedelta, timezone
import json
import random
import uuid

from shadowline.config.line_loader import LineLoader
from shadowline.config.settings import ShadowLineSettings
from shadowline.domain.enums import AlertSeverity, AlertStatus, ConfidenceTier, EventType, PredictionType
from shadowline.domain.evidence import EvidenceItem, Explanation
from shadowline.domain.prediction import Prediction
from shadowline.persistence.engine import get_db_engine, init_db
from shadowline.persistence.models import (
    AlertModel,
    EventModel,
    GenealogyModel,
    PredictionModel,
    ScorecardModel,
    StationHistoryModel,
)
from shadowline.trust.scorecard import ScorecardCalculator


def seed_database():
    settings = ShadowLineSettings()
    init_db(settings.db_url)
    engine = get_db_engine(settings.db_url)
    topology = LineLoader.load_from_yaml(settings.line_config)

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()

    print(f"Seeding database at {settings.db_url}...")

    now = datetime.now(timezone.utc)
    base_time = now - timedelta(days=2)

    station_ids = list(topology.stations.keys())

    # 1. Seed Station History and Events
    print("Generating historical events and station state transitions...")
    events = []
    station_history = []
    genealogy_records = []

    for i in range(100):
        vin = f"VIN-2026-HIST-{i:05d}"
        variant = random.choice(["SUV_A", "SEDAN_B", "EV_C"])
        t_unit = base_time + timedelta(minutes=i * 2.5)

        for s_id in station_ids[:15]:
            st_info = topology.stations[s_id]
            ct = random.gauss(st_info.nominal_cycle_time, 1.5)
            t_enter = t_unit
            t_exit = t_enter + timedelta(seconds=ct)
            t_unit = t_exit

            # Event: State Change
            ev_state = EventModel(
                event_id=str(uuid.uuid4()),
                event_type=EventType.STATION_STATE_CHANGED.value,
                occurred_at=t_enter,
                ingested_at=t_enter + timedelta(seconds=0.1),
                station_id=s_id,
                zone=st_info.zone.value,
                confidence_tier=st_info.confidence_tier.value,
                source="simulated",
                payload_json=json.dumps({"state": "ACTIVE", "vin": vin, "cycle_time_seconds": ct}),
            )
            events.append(ev_state)

            # Station History
            sh = StationHistoryModel(
                station_id=s_id,
                state="ACTIVE",
                cycle_time_seconds=ct,
                vin=vin,
                occurred_at=t_enter,
            )
            station_history.append(sh)

            # Event: Unit Exit
            ev_exit = EventModel(
                event_id=str(uuid.uuid4()),
                event_type=EventType.UNIT_EXITED_STATION.value,
                occurred_at=t_exit,
                ingested_at=t_exit + timedelta(seconds=0.1),
                station_id=s_id,
                zone=st_info.zone.value,
                confidence_tier=st_info.confidence_tier.value,
                source="simulated",
                payload_json=json.dumps({"vin": vin, "variant": variant, "dwell_seconds": ct}),
            )
            events.append(ev_exit)

            # Genealogy
            gn = GenealogyModel(
                vin=vin,
                variant=variant,
                station_id=s_id,
                station_name=st_info.name,
                entered_at=t_enter,
                exited_at=t_exit,
                dwell_seconds=ct,
                defect_codes_json=json.dumps([]),
                measurements_json=json.dumps({"torque_nm": 45.2}),
            )
            genealogy_records.append(gn)

    session.bulk_save_objects(events)
    session.bulk_save_objects(station_history)
    session.bulk_save_objects(genealogy_records)
    session.commit()
    print(f"Saved {len(events)} events and {len(genealogy_records)} genealogy records.")

    # 2. Seed Predictions (for scorecard validation: 85% precision, 5% false alarm rate)
    print("Generating scored predictions for trust scorecard...")
    prediction_models = []
    domain_preds = []

    for i in range(80):
        t_pred = base_time + timedelta(minutes=i * 20)
        s_id = random.choice(station_ids)
        st_info = topology.stations[s_id]

        prob = random.uniform(0.70, 0.95)
        # 92% true positive rate
        actual = random.random() < 0.92

        exp = Explanation(
            summary=f"Bottleneck predicted at {s_id} with probability {prob:.2f}",
            key_factors=["Nominal cycle time near takt", "Accumulated upstream buffer"],
            evidence_items=[EvidenceItem("mc_prob", prob, 0.50, "prob", "Simulated run probability")],
            recommended_actions=["Inspect station cycle time."],
        )

        pred_obj = Prediction.create(
            prediction_type=PredictionType.BOTTLENECK,
            subject_id=s_id,
            horizon_hours=1.0,
            probability=prob,
            calibrated_probability=prob,
            confidence_tier=st_info.confidence_tier,
            expected_impact_time=t_pred + timedelta(hours=1.0),
            predicted_state="ACTIVE",
            explanation=exp,
        )
        pred_obj.predicted_at = t_pred
        pred_obj.is_scored = True
        pred_obj.actual_outcome = actual
        pred_obj.scored_at = t_pred + timedelta(hours=1.0)
        domain_preds.append(pred_obj)

        pm = PredictionModel(
            id=pred_obj.id,
            prediction_type=pred_obj.prediction_type.value,
            subject_id=pred_obj.subject_id,
            predicted_at=pred_obj.predicted_at,
            horizon_hours=pred_obj.horizon_hours,
            probability=pred_obj.probability,
            calibrated_probability=pred_obj.calibrated_probability,
            confidence_tier=pred_obj.confidence_tier.value,
            expected_impact_time=pred_obj.expected_impact_time,
            predicted_state=pred_obj.predicted_state,
            explanation_json=json.dumps(exp.__dict__, default=str),
            metadata_json=json.dumps({}),
            is_scored=True,
            actual_outcome=actual,
            scored_at=pred_obj.scored_at,
        )
        prediction_models.append(pm)

    session.bulk_save_objects(prediction_models)
    session.commit()
    print(f"Saved {len(prediction_models)} scored predictions.")

    # 3. Seed Scorecard
    scorecard = ScorecardCalculator.calculate(domain_preds)
    sc_model = ScorecardModel(
        total_predictions=scorecard.total_predictions,
        scored_predictions=scorecard.scored_predictions,
        true_positives=scorecard.true_positives,
        false_positives=scorecard.false_positives,
        true_negatives=scorecard.true_negatives,
        false_negatives=scorecard.false_negatives,
        precision=scorecard.precision,
        recall=scorecard.recall,
        false_alarm_rate=scorecard.false_alarm_rate,
        mean_lead_time_minutes=scorecard.mean_lead_time_minutes,
        brier_score=scorecard.reliability_data.brier_score,
        is_live_promoted=True,
    )
    session.add(sc_model)
    session.commit()
    print(f"Saved trust scorecard: Precision={scorecard.precision:.2f}, FAR={scorecard.false_alarm_rate:.2f}")

    session.close()
    print("Database seeding completed successfully.")


if __name__ == "__main__":
    seed_database()
