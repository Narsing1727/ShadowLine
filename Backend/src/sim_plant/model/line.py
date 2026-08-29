"""Simulated line model wiring all stations, buffers, and unit generator."""

import random
import simpy
from typing import Any, Callable, Dict, List, Optional
from sim_plant.model.buffer import SimBuffer
from sim_plant.model.station import SimStation
from sim_plant.model.unit import SimUnit
from sim_plant.model.variant_profile import VariantProfile, parse_variant_profiles


class SimLine:
    def __init__(
        self,
        env: simpy.Environment,
        line_config: Dict[str, Any],
        variants_config: Dict[str, Any],
        emit_callback: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    ):
        self.env = env
        self.line_config = line_config
        self.variants_config = variants_config
        self.emit_callback = emit_callback

        self.takt_time = float(line_config.get("takt_time_seconds", 58.0))
        self.variant_profiles = parse_variant_profiles(variants_config)
        self.variant_keys = list(self.variant_profiles.keys())
        self.variant_probs = [p.production_share for p in self.variant_profiles.values()]
        # normalize probabilities
        total_p = sum(self.variant_probs)
        self.variant_probs = [p / total_p for p in self.variant_probs] if total_p > 0 else [1.0]

        self.buffers: Dict[str, SimBuffer] = {}
        self.stations: Dict[str, SimStation] = {}
        self.station_sequence: List[str] = []
        self.units_produced: List[SimUnit] = []
        self.unit_counter = 0

        self._build_topology()
        self.generator_proc = env.process(self._unit_generator())

    def _build_topology(self):
        # 1. Create buffers
        raw_buffers = self.line_config.get("buffers", [])
        for b in raw_buffers:
            s_buf = SimBuffer(
                env=self.env,
                buffer_id=b["id"],
                capacity=b["capacity"],
                upstream_id=b["upstream_station_id"],
                downstream_id=b["downstream_station_id"],
            )
            self.buffers[b["id"]] = s_buf

        # 2. Map buffers to stations
        raw_stations = self.line_config.get("stations", [])
        for i, s in enumerate(raw_stations):
            s_id = s["id"]
            self.station_sequence.append(s_id)

            # Find in_buffer (where downstream == s_id)
            in_buf = None
            for b in self.buffers.values():
                if b.downstream_id == s_id:
                    in_buf = b
                    break

            # If it's the very first station, create an entry buffer
            if i == 0 and in_buf is None:
                in_buf = SimBuffer(self.env, "B-ENTRY", capacity=100, upstream_id="ENTRY", downstream_id=s_id)
                self.entry_buffer = in_buf

            # Find out_buffer (where upstream == s_id)
            out_buf = None
            for b in self.buffers.values():
                if b.upstream_id == s_id:
                    out_buf = b
                    break

            station = SimStation(
                env=self.env,
                station_id=s_id,
                name=s["name"],
                zone=s["zone"],
                confidence_tier=s["confidence_tier"],
                nominal_cycle_time=float(s["nominal_cycle_time"]),
                in_buffer=in_buf,
                out_buffer=out_buf,
                emit_callback=self._handle_station_emit,
            )
            self.stations[s_id] = station

    def _handle_station_emit(self, event_type: str, payload: Dict[str, Any]):
        # Defect baseline logic for UNIT_EXITED_STATION
        if event_type == "UNIT_EXITED_STATION":
            vin = payload.get("vin")
            station_id = payload.get("station_id")
            variant = payload.get("variant")
            profile = self.variant_profiles.get(variant)
            if profile:
                for db in profile.defect_baselines:
                    # If this station is the causing station, roll for defect injection
                    if db.causing_station_id == station_id:
                        station_obj = self.stations.get(station_id)
                        mult = station_obj.defect_probability_multiplier if station_obj else 1.0
                        if random.random() < (db.base_probability * mult):
                            # Mark defect on unit in sim_plant
                            payload["defect_injected"] = db.defect_code

                    # If this station is the detecting station, check if unit had this defect
                    if db.detecting_station_id == station_id:
                        # With probability, detect it and emit DEFECT_DETECTED
                        if random.random() < 0.85:  # detection efficiency
                            if self.emit_callback:
                                self.emit_callback(
                                    "DEFECT_DETECTED",
                                    {
                                        "vin": vin,
                                        "defect_code": db.defect_code,
                                        "detecting_station_id": station_id,
                                        "zone": payload.get("zone"),
                                        "confidence_tier": payload.get("confidence_tier"),
                                    },
                                )

        if self.emit_callback:
            self.emit_callback(event_type, payload)

    def _unit_generator(self):
        while True:
            self.unit_counter += 1
            variant = random.choices(self.variant_keys, weights=self.variant_probs, k=1)[0]
            unit = SimUnit.create(variant, self.env.now, self.unit_counter)

            # Put into first station's entry buffer
            first_station = self.stations[self.station_sequence[0]]
            if first_station.in_buffer:
                yield first_station.in_buffer.put(unit)

            # Inter-arrival cadence around takt time with slight variance
            yield self.env.timeout(max(15.0, random.gauss(self.takt_time, 3.0)))
