"""Sudden breakdown failure fault implementation."""

import simpy
from typing import Any


def run_sudden_failure(
    env: simpy.Environment,
    station: Any,
    start_time_seconds: float,
    duration_seconds: float,
):
    """Brings station down abruptly after start_time_seconds for duration_seconds."""
    yield env.timeout(start_time_seconds)
    yield station.trigger_down(duration_seconds)
