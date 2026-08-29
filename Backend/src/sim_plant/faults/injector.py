"""Fault injector scheduling fault scenarios from config."""

from typing import Any, Dict, List
import simpy
from sim_plant.faults.gradual_drift import run_gradual_drift
from sim_plant.faults.intermittent import run_intermittent_fault
from sim_plant.faults.sudden_failure import run_sudden_failure


class FaultInjector:
    def __init__(self, env: simpy.Environment, stations: Dict[str, Any], faults_config: Dict[str, Any]):
        self.env = env
        self.stations = stations
        self.faults_config = faults_config
        self.scheduled_faults = faults_config.get("faults", [])

    def schedule_all(self):
        for f in self.scheduled_faults:
            s_id = f["station_id"]
            station = self.stations.get(s_id)
            if not station:
                continue

            f_type = f.get("type")
            start_sec = float(f.get("start_time_minutes", 0.0)) * 60.0
            duration_sec = float(f.get("duration_minutes", 10.0)) * 60.0

            if f_type == "gradual_drift":
                ct_inc = float(f.get("cycle_time_increase_pct", 0.15))
                def_mult = float(f.get("defect_probability_multiplier", 3.0))
                self.env.process(
                    run_gradual_drift(
                        self.env,
                        station,
                        start_time_seconds=start_sec,
                        duration_seconds=duration_sec,
                        cycle_time_increase_pct=ct_inc,
                        defect_multiplier=def_mult,
                    )
                )
            elif f_type == "sudden_failure":
                self.env.process(
                    run_sudden_failure(
                        self.env,
                        station,
                        start_time_seconds=start_sec,
                        duration_seconds=duration_sec,
                    )
                )
            elif f_type == "intermittent":
                flicker_int = float(f.get("flicker_interval_seconds", 45.0))
                down_dur = float(f.get("down_duration_seconds", 15.0))
                def_mult = float(f.get("defect_probability_multiplier", 2.5))
                self.env.process(
                    run_intermittent_fault(
                        self.env,
                        station,
                        start_time_seconds=start_sec,
                        duration_seconds=duration_sec,
                        flicker_interval_seconds=flicker_int,
                        down_duration_seconds=down_dur,
                        defect_multiplier=def_mult,
                    )
                )
