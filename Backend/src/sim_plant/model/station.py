"""SimPy station process representing assembly stations."""

import random
import simpy
from typing import Any, Callable, Dict, Optional
from sim_plant.model.unit import SimUnit
from sim_plant.model.variant_profile import VariantProfile


class SimStation:
    def __init__(
        self,
        env: simpy.Environment,
        station_id: str,
        name: str,
        zone: str,
        confidence_tier: str,
        nominal_cycle_time: float,
        in_buffer: Optional[Any],
        out_buffer: Optional[Any],
        emit_callback: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    ):
        self.env = env
        self.station_id = station_id
        self.name = name
        self.zone = zone
        self.confidence_tier = confidence_tier
        self.nominal_cycle_time = nominal_cycle_time
        self.in_buffer = in_buffer
        self.out_buffer = out_buffer
        self.emit_callback = emit_callback

        self.current_state = "IDLE"
        self.current_unit: Optional[SimUnit] = None
        self.cycle_time_drift_factor = 1.0
        self.defect_probability_multiplier = 1.0
        self.is_down = False
        self.down_event: Optional[simpy.Event] = None
        self.process = env.process(self.run())

    def _set_state(self, new_state: str, cycle_time_seconds: Optional[float] = None) -> None:
        prev = self.current_state
        self.current_state = new_state
        if self.emit_callback:
            self.emit_callback(
                "STATION_STATE_CHANGED",
                {
                    "station_id": self.station_id,
                    "zone": self.zone,
                    "confidence_tier": self.confidence_tier,
                    "state": new_state,
                    "previous_state": prev,
                    "cycle_time_seconds": cycle_time_seconds,
                    "vin": self.current_unit.vin if self.current_unit else None,
                },
            )

    def trigger_down(self, duration_seconds: float):
        """Called by fault injector to bring station down."""
        def _down_proc():
            self.is_down = True
            prev_state = self.current_state
            self._set_state("DOWN")
            yield self.env.timeout(duration_seconds)
            self.is_down = False
            self._set_state(prev_state if prev_state != "DOWN" else "IDLE")

        return self.env.process(_down_proc())

    def run(self):
        while True:
            # 1. Fetch unit from in_buffer (if any)
            if self.in_buffer:
                if self.in_buffer.occupancy == 0:
                    self._set_state("STARVED")
                unit: SimUnit = yield self.in_buffer.get()
            else:
                # First station in line waits for generated units or spawns
                yield self.env.timeout(1.0)
                continue

            self.current_unit = unit
            unit.record_station_entry(self.station_id, self.env.now)

            # Wait if currently down
            while self.is_down:
                yield self.env.timeout(1.0)

            # 2. Process unit
            self._set_state("ACTIVE")
            
            # Base cycle time with slight Gaussian noise
            base_ct = self.nominal_cycle_time * self.cycle_time_drift_factor
            actual_ct = max(10.0, random.gauss(base_ct, 2.0))

            yield self.env.timeout(actual_ct)

            # Wait if went down during processing
            while self.is_down:
                yield self.env.timeout(1.0)

            unit.record_station_exit(self.station_id, self.env.now)

            # Check for defect creation or detection
            if self.emit_callback:
                self.emit_callback(
                    "UNIT_EXITED_STATION",
                    {
                        "station_id": self.station_id,
                        "zone": self.zone,
                        "confidence_tier": self.confidence_tier,
                        "vin": unit.vin,
                        "variant": unit.variant,
                        "dwell_seconds": actual_ct,
                    },
                )

            # 3. Output to out_buffer (if any)
            if self.out_buffer:
                if self.out_buffer.is_full:
                    self._set_state("BLOCKED", cycle_time_seconds=actual_ct)
                yield self.out_buffer.put(unit)
            
            self._set_state("IDLE", cycle_time_seconds=actual_ct)
            self.current_unit = None
