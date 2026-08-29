"""Observability metrics tracking."""

from dataclasses import dataclass
import threading
from typing import Dict


@dataclass
class SystemMetrics:
    cycles_completed: int = 0
    total_predictions_generated: int = 0
    total_alerts_surfaced: int = 0
    total_alerts_suppressed: int = 0
    last_cycle_duration_seconds: float = 0.0


class MetricsCollector:
    """Thread-safe lightweight metrics registry."""

    def __init__(self):
        self._lock = threading.Lock()
        self._metrics = SystemMetrics()

    def record_cycle(
        self,
        duration_seconds: float,
        predictions_count: int,
        alerts_count: int,
        suppressed_count: int,
    ) -> None:
        with self._lock:
            self._metrics.cycles_completed += 1
            self._metrics.last_cycle_duration_seconds = round(duration_seconds, 3)
            self._metrics.total_predictions_generated += predictions_count
            self._metrics.total_alerts_surfaced += alerts_count
            self._metrics.total_alerts_suppressed += suppressed_count

    def get_metrics(self) -> Dict[str, float]:
        with self._lock:
            return {
                "cycles_completed": self._metrics.cycles_completed,
                "total_predictions_generated": self._metrics.total_predictions_generated,
                "total_alerts_surfaced": self._metrics.total_alerts_surfaced,
                "total_alerts_suppressed": self._metrics.total_alerts_suppressed,
                "last_cycle_duration_seconds": self._metrics.last_cycle_duration_seconds,
            }
