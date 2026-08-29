"""Gradual process drift fault implementation."""

import simpy
from typing import Any


def run_gradual_drift(
    env: simpy.Environment,
    station: Any,
    start_time_seconds: float,
    duration_seconds: float,
    cycle_time_increase_pct: float = 0.15,
    defect_multiplier: float = 3.0,
):
    """Gradually drifts station cycle time and defect probability up over duration."""
    yield env.timeout(start_time_seconds)
    
    steps = 10
    step_duration = duration_seconds / steps
    ct_step = cycle_time_increase_pct / steps
    defect_step = (defect_multiplier - 1.0) / steps

    for _ in range(steps):
        yield env.timeout(step_duration)
        station.cycle_time_drift_factor += ct_step
        station.defect_probability_multiplier += defect_step
