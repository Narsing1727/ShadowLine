"""Unit tests for lag estimation and defect propagation."""

from shadowline.prediction.defect.backward_trace import DefectBackwardTracer
from shadowline.prediction.defect.drift_detector import ProcessDriftDetector
from shadowline.prediction.defect.lag_estimator import DefectLagEstimator
from shadowline.prediction.defect.propagation_graph import DefectPropagationGraph


def test_lag_estimator_and_graph():
    estimator = DefectLagEstimator()
    estimator.record_lag("S-03", "S-11", "D-WELD-01", 18.0)
    estimator.record_lag("S-03", "S-11", "D-WELD-01", 20.0)
    estimator.record_lag("S-03", "S-11", "D-WELD-01", 16.0)

    est = estimator.estimate("S-03", "S-11", "D-WELD-01")
    assert est is not None
    assert est.sample_count == 3
    assert est.mean_lag_minutes == 18.0

    # Propagation graph
    graph = DefectPropagationGraph()
    graph.add_or_update_edge("S-03", "S-11", "D-WELD-01", 18.0)
    graph.add_or_update_edge("S-03", "S-11", "D-WELD-01", 20.0)

    causes = graph.get_candidate_causes("S-11")
    assert len(causes) == 1
    assert causes[0]["causing_station_id"] == "S-03"
    assert causes[0]["observed_cases"] == 2

    # Backward tracer
    tracer = DefectBackwardTracer(graph)
    candidates = tracer.trace("D-WELD-01", "S-11")
    assert len(candidates) >= 1
    assert candidates[0].station_id == "S-03"


def test_process_drift_detector():
    detector = ProcessDriftDetector(z_score_threshold=2.0)
    # Drifting cycle times (nominal 50s -> drifting to 65s)
    cycle_times = [50.0] * 20 + [65.0] * 10
    res = detector.detect_cycle_time_drift("S-14", cycle_times, nominal_cycle_time=50.0)
    assert res.is_drifting is True
    assert res.z_score > 2.0
