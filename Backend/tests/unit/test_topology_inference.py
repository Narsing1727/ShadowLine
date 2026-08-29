"""Unit tests for topology and buffer discovery inference."""

from shadowline.discovery.buffer_inference import BufferInferenceEngine
from shadowline.discovery.takt_estimator import TaktEstimator
from shadowline.discovery.topology_inference import TopologyInferenceEngine


def test_topology_and_buffer_inference():
    # Synthetic unit exit events where S-01 -> S-02 -> S-03
    events = []
    for i in range(30):
        vin = f"VIN-{i:03d}"
        t_base = i * 60.0
        events.append({"vin": vin, "station_id": "S-01", "timestamp": t_base + 10.0})
        events.append({"vin": vin, "station_id": "S-02", "timestamp": t_base + 70.0})
        events.append({"vin": vin, "station_id": "S-03", "timestamp": t_base + 130.0})

    inferred_top = TopologyInferenceEngine.infer_sequence(events)
    assert inferred_top.station_sequence == ["S-01", "S-02", "S-03"]
    assert inferred_top.confidence_score >= 0.95

    # Takt estimation
    s03_ts = [e["timestamp"] for e in events if e["station_id"] == "S-03"]
    takt = TaktEstimator.estimate_takt(s03_ts)
    assert 55.0 <= takt <= 65.0

    # Buffer inference
    buffers = BufferInferenceEngine.infer_buffers(
        station_sequence=inferred_top.station_sequence,
        unit_exit_events=events,
        nominal_cycle_time=55.0,
    )
    assert len(buffers) == 2
    assert buffers[0].upstream_station_id == "S-01"
    assert buffers[0].downstream_station_id == "S-02"
    assert buffers[0].estimated_capacity >= 1
