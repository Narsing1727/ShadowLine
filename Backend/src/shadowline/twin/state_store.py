"""Real-time in-memory state store for the ShadowLine Digital Twin."""

from datetime import datetime, timezone
import logging
import threading
from typing import Any, Dict, List, Optional

from shadowline.domain.buffer import Buffer
from shadowline.domain.enums import ConfidenceTier, EventType, StationState, Variant, Zone
from shadowline.domain.events import CanonicalEvent
from shadowline.domain.station import Station
from shadowline.domain.topology import Topology
from shadowline.domain.unit import Unit
from shadowline.twin.genealogy_tracker import GenealogyTracker
from shadowline.twin.snapshot import BufferSnapshot, StationSnapshot, TwinSnapshot, UnitSnapshot

logger = logging.getLogger("shadowline.twin.state_store")


class StateStore:
    """Thread-safe live in-memory digital twin state store."""

    def __init__(self, topology: Topology):
        self._lock = threading.RLock()
        self.topology = topology
        self.stations: Dict[str, Station] = dict(topology.stations)
        self.buffers: Dict[str, Buffer] = dict(topology.buffers)
        self.in_flight_units: Dict[str, Unit] = {}
        self.genealogy_tracker = GenealogyTracker()
        self.last_updated_at: datetime = datetime.now(timezone.utc)
        self.total_events_processed: int = 0
        self.cycle_time_history: Dict[str, List[float]] = {s_id: [] for s_id in self.stations}

    def apply_event(self, event: CanonicalEvent) -> None:
        with self._lock:
            self.total_events_processed += 1
            self.last_updated_at = event.occurred_at

            if event.event_type == EventType.STATION_STATE_CHANGED:
                self._handle_state_changed(event)
            elif event.event_type == EventType.UNIT_EXITED_STATION:
                self._handle_unit_exited(event)
            elif event.event_type == EventType.DEFECT_DETECTED:
                self._handle_defect_detected(event)

    def _handle_state_changed(self, event: CanonicalEvent) -> None:
        station_id = event.station_id
        if not station_id or station_id not in self.stations:
            return

        station = self.stations[station_id]
        payload = event.payload or {}
        new_state_str = payload.get("state", "IDLE")

        try:
            new_state = StationState(new_state_str)
        except ValueError:
            new_state = StationState.IDLE

        # Update time in state if previous state existed
        if station.last_state_change:
            duration = (event.occurred_at - station.last_state_change).total_seconds()
            if duration > 0:
                if station.current_state == StationState.ACTIVE:
                    station.active_period_seconds += duration
                elif station.current_state == StationState.BLOCKED:
                    station.blocked_period_seconds += duration
                elif station.current_state == StationState.STARVED:
                    station.starved_period_seconds += duration
                elif station.current_state == StationState.DOWN:
                    station.down_period_seconds += duration

        station.current_state = new_state
        station.last_state_change = event.occurred_at

        ct = payload.get("cycle_time_seconds")
        if ct is not None:
            station.last_cycle_time = float(ct)
            self.cycle_time_history[station_id].append(float(ct))
            if len(self.cycle_time_history[station_id]) > 500:
                self.cycle_time_history[station_id].pop(0)

        vin = payload.get("vin")
        if vin:
            station.current_unit_vin = vin

    def _handle_unit_exited(self, event: CanonicalEvent) -> None:
        station_id = event.station_id
        payload = event.payload or {}
        vin = payload.get("vin")
        variant_str = payload.get("variant", "SUV_A")
        dwell = payload.get("dwell_seconds")

        try:
            variant = Variant(variant_str)
        except ValueError:
            variant = Variant.SUV_A

        if station_id and station_id in self.stations:
            station = self.stations[station_id]
            station.total_units_processed += 1
            if station.current_unit_vin == vin:
                station.current_unit_vin = None

            # Update genealogy
            self.genealogy_tracker.record_exit(vin, station_id, event.occurred_at, dwell)

            # Update buffers
            # Unit leaving station goes into downstream buffer
            for buf in self.buffers.values():
                if buf.upstream_station_id == station_id:
                    if buf.current_occupancy < buf.capacity:
                        buf.current_occupancy += 1
                        buf.queued_vins.append(vin)
                    break
                # Unit being processed by station leaves upstream buffer
                if buf.downstream_station_id == station_id:
                    if buf.current_occupancy > 0:
                        buf.current_occupancy -= 1
                        if vin in buf.queued_vins:
                            buf.queued_vins.remove(vin)
                    break

        if vin:
            if vin not in self.in_flight_units:
                self.in_flight_units[vin] = Unit(
                    vin=vin,
                    variant=variant,
                    entered_line_at=event.occurred_at,
                    current_station_id=station_id,
                )
            else:
                self.in_flight_units[vin].current_station_id = station_id

    def _handle_defect_detected(self, event: CanonicalEvent) -> None:
        payload = event.payload or {}
        vin = payload.get("vin")
        defect_code = payload.get("defect_code")
        detecting_station_id = payload.get("detecting_station_id") or event.station_id

        if vin and defect_code and detecting_station_id:
            self.genealogy_tracker.record_defect(
                vin=vin,
                defect_code=defect_code,
                detecting_station_id=detecting_station_id,
                detected_at=event.occurred_at,
            )
            if vin in self.in_flight_units:
                self.in_flight_units[vin].defect_codes.append(defect_code)

    def snapshot(self) -> TwinSnapshot:
        with self._lock:
            station_snaps = {
                s.id: StationSnapshot(
                    id=s.id,
                    name=s.name,
                    zone=s.zone.value if hasattr(s.zone, "value") else str(s.zone),
                    confidence_tier=s.confidence_tier.value if hasattr(s.confidence_tier, "value") else str(s.confidence_tier),
                    nominal_cycle_time=s.nominal_cycle_time,
                    current_state=s.current_state.value if hasattr(s.current_state, "value") else str(s.current_state),
                    current_unit_vin=s.current_unit_vin,
                    last_cycle_time=s.last_cycle_time,
                    active_period_seconds=s.active_period_seconds,
                    blocked_period_seconds=s.blocked_period_seconds,
                    starved_period_seconds=s.starved_period_seconds,
                    down_period_seconds=s.down_period_seconds,
                    total_units_processed=s.total_units_processed,
                )
                for s in self.stations.values()
            }

            buffer_snaps = {
                b.id: BufferSnapshot(
                    id=b.id,
                    upstream_station_id=b.upstream_station_id,
                    downstream_station_id=b.downstream_station_id,
                    capacity=b.capacity,
                    current_occupancy=b.current_occupancy,
                    queued_vins=list(b.queued_vins),
                )
                for b in self.buffers.values()
            }

            unit_snaps = {
                u.vin: UnitSnapshot(
                    vin=u.vin,
                    variant=u.variant.value if hasattr(u.variant, "value") else str(u.variant),
                    entered_line_at=u.entered_line_at.isoformat(),
                    current_station_id=u.current_station_id,
                    defect_codes=list(u.defect_codes),
                )
                for u in self.in_flight_units.values()
            }

            return TwinSnapshot(
                timestamp=self.last_updated_at,
                stations=station_snaps,
                buffers=buffer_snaps,
                in_flight_units=unit_snaps,
            )
