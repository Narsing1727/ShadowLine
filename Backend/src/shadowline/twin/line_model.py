"""SimPy-based twin line simulation model used for forking and forecasting."""

import random
import simpy
from typing import Any, Dict, List, Optional
from shadowline.twin.snapshot import TwinSnapshot


class ForkedStation:
    def __init__(
        self,
        env: simpy.Environment,
        station_id: str,
        nominal_cycle_time: float,
        in_store: Optional[simpy.Store],
        out_store: Optional[simpy.Store],
        initial_state: str = "IDLE",
    ):
        self.env = env
        self.station_id = station_id
        self.nominal_cycle_time = nominal_cycle_time
        self.in_store = in_store
        self.out_store = out_store
        self.state = initial_state
        self.active_time = 0.0
        self.blocked_time = 0.0
        self.starved_time = 0.0
        self.units_completed = 0
        self.process = env.process(self.run())

    def run(self):
        while True:
            # 1. Infeed
            if self.in_store:
                if len(self.in_store.items) == 0:
                    self.state = "STARVED"
                t0 = self.env.now
                unit = yield self.in_store.get()
                self.starved_time += max(0.0, self.env.now - t0)
            else:
                yield self.env.timeout(1.0)
                continue

            # 2. Process
            self.state = "ACTIVE"
            ct = max(10.0, random.gauss(self.nominal_cycle_time, 2.0))
            t_proc_start = self.env.now
            yield self.env.timeout(ct)
            self.active_time += (self.env.now - t_proc_start)
            self.units_completed += 1

            # 3. Outfeed
            if self.out_store:
                if len(self.out_store.items) >= self.out_store.capacity:
                    self.state = "BLOCKED"
                t_block_start = self.env.now
                yield self.out_store.put(unit)
                self.blocked_time += max(0.0, self.env.now - t_block_start)

            self.state = "IDLE"


class TwinLineModel:
    """Discrete-event SimPy model of the twin initialized from a snapshot."""

    def __init__(self, snapshot: TwinSnapshot, takt_time: float = 58.0):
        self.snapshot = snapshot
        self.takt_time = takt_time
        self.env = simpy.Environment()
        self.stores: Dict[str, simpy.Store] = {}
        self.stations: Dict[str, ForkedStation] = {}
        self.unit_counter = 0

        self._build_model()
        self.env.process(self._generator())

    def _build_model(self):
        # 1. Build buffer stores
        for b_id, b_snap in self.snapshot.buffers.items():
            store = simpy.Store(self.env, capacity=max(1, b_snap.capacity))
            # Seed buffer with existing units
            for _ in range(b_snap.current_occupancy):
                store.items.append({"vin": f"VIN-PREV-{random.randint(1000, 9999)}"})
            self.stores[b_id] = store

        # 2. Build stations
        sorted_station_ids = list(self.snapshot.stations.keys())
        for i, s_id in enumerate(sorted_station_ids):
            s_snap = self.snapshot.stations[s_id]

            # In store
            in_store = None
            for b_id, b_snap in self.snapshot.buffers.items():
                if b_snap.downstream_station_id == s_id:
                    in_store = self.stores.get(b_id)
                    break

            if i == 0 and in_store is None:
                in_store = simpy.Store(self.env, capacity=100)
                self.entry_store = in_store

            # Out store
            out_store = None
            for b_id, b_snap in self.snapshot.buffers.items():
                if b_snap.upstream_station_id == s_id:
                    out_store = self.stores.get(b_id)
                    break

            station = ForkedStation(
                env=self.env,
                station_id=s_id,
                nominal_cycle_time=s_snap.nominal_cycle_time,
                in_store=in_store,
                out_store=out_store,
                initial_state=s_snap.current_state,
            )
            self.stations[s_id] = station

    def _generator(self):
        first_station_id = list(self.snapshot.stations.keys())[0]
        first_st = self.stations[first_station_id]
        while True:
            self.unit_counter += 1
            if first_st.in_store:
                yield first_st.in_store.put({"vin": f"VIN-SIM-{self.unit_counter}"})
            yield self.env.timeout(max(15.0, random.gauss(self.takt_time, 2.5)))
