"""Integration test: Ingestion -> Normalizer -> State Store -> Snapshot."""

from datetime import datetime, timezone
import pytest
from shadowline.domain.enums import ConfidenceTier, EventType, StationState
from shadowline.ingestion.adapters.simulated import SimulatedIngestionAdapter
from shadowline.ingestion.normalizer import EventNormalizer
from shadowline.twin.state_store import StateStore


def test_ingestion_to_twin_pipeline(state_store: StateStore):
    adapter = SimulatedIngestionAdapter()

    # 1. State change event
    raw_state = {
        "event_id": "evt-001",
        "event_type": "STATION_STATE_CHANGED",
        "occurred_at": datetime.now(timezone.utc).isoformat(),
        "station_id": "S-01",
        "zone": "BODY_SHOP",
        "confidence_tier": "MEASURED",
        "payload": {"state": "ACTIVE", "vin": "VIN-TEST-100", "cycle_time_seconds": 54.5},
    }
    adapter.inject_event(raw_state)

    evt = adapter._queue.get_nowait()
    state_store.apply_event(evt)

    # Verify station state updated
    assert state_store.stations["S-01"].current_state == StationState.ACTIVE
    assert state_store.stations["S-01"].last_cycle_time == 54.5
    assert state_store.stations["S-01"].current_unit_vin == "VIN-TEST-100"

    # 2. Unit exit event
    raw_exit = {
        "event_id": "evt-002",
        "event_type": "UNIT_EXITED_STATION",
        "occurred_at": datetime.now(timezone.utc).isoformat(),
        "station_id": "S-01",
        "zone": "BODY_SHOP",
        "confidence_tier": "MEASURED",
        "payload": {"vin": "VIN-TEST-100", "variant": "SUV_A", "dwell_seconds": 54.5},
    }
    adapter.inject_event(raw_exit)

    evt2 = adapter._queue.get_nowait()
    state_store.apply_event(evt2)

    assert state_store.stations["S-01"].total_units_processed == 1
    assert "VIN-TEST-100" in state_store.in_flight_units
    # Unit entered buffer B-01 downstream of S-01
    assert state_store.buffers["B-01"].current_occupancy == 1
    assert "VIN-TEST-100" in state_store.buffers["B-01"].queued_vins

    # Verify snapshot integrity
    snap = state_store.snapshot()
    assert snap.stations["S-01"].total_units_processed == 1
    assert snap.buffers["B-01"].current_occupancy == 1
