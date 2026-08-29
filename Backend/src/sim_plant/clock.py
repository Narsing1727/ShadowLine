"""Simulation clock to wall-clock time mapping."""

from datetime import datetime, timedelta, timezone


class SimClock:
    def __init__(self, start_time: datetime | None = None, speed_factor: float = 1.0):
        self.start_time = start_time or datetime.now(timezone.utc)
        self.speed_factor = max(0.001, speed_factor)

    def sim_to_datetime(self, sim_now_seconds: float) -> datetime:
        """Converts simpy environment time (in seconds) to UTC datetime."""
        return self.start_time + timedelta(seconds=sim_now_seconds)

    def datetime_to_sim(self, dt: datetime) -> float:
        """Converts UTC datetime back to simpy environment time (in seconds)."""
        delta = dt - self.start_time
        return max(0.0, delta.total_seconds())
