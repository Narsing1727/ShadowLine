"""Intermittent flickering fault implementation."""

import simpy
from typing import Any


def run_intermittent_fault(
    env: simpy.Environment,
    station: Any,
    start_time_seconds: float,
    duration_seconds: float,
    flicker_interval_seconds: float = 45.0,
    down_duration_seconds: float = 15.0,
    defect_multiplier: float = 2.5,
):
    """Intermittently brings station down at short intervals and increases defects."""
    yield env.timeout(start_time_seconds)
    station.defect_probability_multiplier = defect_multiplier

    end_time = start_time_seconds + duration_seconds
    while env.now < end_time:
        yield station.trigger_down(down_duration_seconds)
        yield env.timeout(flicker_interval_seconds)

    station.defect_probability_multiplier = 1.0
