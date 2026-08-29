"""Defect prediction and root-cause tracing package."""

from shadowline.prediction.defect.backward_trace import BackwardTraceCandidate, DefectBackwardTracer
from shadowline.prediction.defect.containment import ContainmentReport, DefectContainmentEngine
from shadowline.prediction.defect.drift_detector import DriftDetectionResult, ProcessDriftDetector
from shadowline.prediction.defect.lag_estimator import DefectLagEstimator, LagEstimate
from shadowline.prediction.defect.propagation_graph import DefectPropagationGraph, PropagationEdge

__all__ = [
    "BackwardTraceCandidate",
    "ContainmentReport",
    "DefectBackwardTracer",
    "DefectContainmentEngine",
    "DefectLagEstimator",
    "DefectPropagationGraph",
    "DriftDetectionResult",
    "LagEstimate",
    "ProcessDriftDetector",
    "PropagationEdge",
]
