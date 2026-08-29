"""Simulation advance engine for forward forecasting."""

from dataclasses import dataclass
from typing import Dict
from shadowline.twin.line_model import TwinLineModel


@dataclass
class AdvanceResult:
    sim_duration_seconds: float
    station_active_times: Dict[str, float]
    station_blocked_times: Dict[str, float]
    station_starved_times: Dict[str, float]
    units_completed: Dict[str, int]
    bottleneck_station_id: str


class TwinAdvancer:
    """Advances forked digital twin forward in simulated time."""

    @staticmethod
    def advance(forked_twin: TwinLineModel, horizon_seconds: float) -> AdvanceResult:
        forked_twin.env.run(until=horizon_seconds)

        active_times = {}
        blocked_times = {}
        starved_times = {}
        units_done = {}

        max_active = -1.0
        bottleneck_id = list(forked_twin.stations.keys())[0]

        for s_id, st in forked_twin.stations.items():
            active_times[s_id] = st.active_time
            blocked_times[s_id] = st.blocked_time
            starved_times[s_id] = st.starved_time
            units_done[s_id] = st.units_completed

            # Active period metric: station with highest active / working ratio is bottleneck
            if st.active_time > max_active:
                max_active = st.active_time
                bottleneck_id = s_id

        return AdvanceResult(
            sim_duration_seconds=horizon_seconds,
            station_active_times=active_times,
            station_blocked_times=blocked_times,
            station_starved_times=starved_times,
            units_completed=units_done,
            bottleneck_station_id=bottleneck_id,
        )
