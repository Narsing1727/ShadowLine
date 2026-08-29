"""Discovery onboarding session managing line reconstruction workflow."""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from shadowline.discovery.buffer_inference import BufferInferenceEngine, InferredBuffer
from shadowline.discovery.parallel_path_detector import ParallelGroup, ParallelPathDetector
from shadowline.discovery.takt_estimator import TaktEstimator
from shadowline.discovery.topology_inference import InferredTopology, TopologyInferenceEngine


@dataclass
class DiscoverySession:
    session_id: str
    line_name: str
    status: str  # INITIALIZED, INGESTING, COMPLETED, FAILED
    created_at: datetime
    updated_at: datetime
    events_ingested: int = 0
    inferred_topology: Optional[InferredTopology] = None
    inferred_buffers: List[InferredBuffer] = field(default_factory=list)
    inferred_parallel_groups: List[ParallelGroup] = field(default_factory=list)
    estimated_takt_time: float = 58.0


class DiscoveryOnboardingManager:
    """Manages discovery and topology onboarding sessions."""

    def __init__(self):
        self._sessions: Dict[str, DiscoverySession] = {}
        self._raw_events: Dict[str, List[Dict[str, float]]] = defaultdict(list)

    def create_session(self, line_name: str) -> DiscoverySession:
        s_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        session = DiscoverySession(
            session_id=s_id,
            line_name=line_name,
            status="INITIALIZED",
            created_at=now,
            updated_at=now,
        )
        self._sessions[s_id] = session
        return session

    def add_events(self, session_id: str, events: List[Dict[str, Any]]) -> None:
        if session_id not in self._sessions:
            return
        session = self._sessions[session_id]
        session.status = "INGESTING"
        session.events_ingested += len(events)
        session.updated_at = datetime.now(timezone.utc)

        for ev in events:
            # Normalize to {'vin': vin, 'station_id': station_id, 'timestamp': ts}
            vin = ev.get("vin") or (ev.get("payload", {}).get("vin"))
            st = ev.get("station_id")
            ts = ev.get("occurred_at") or ev.get("timestamp", 0.0)
            if isinstance(ts, str):
                try:
                    ts = datetime.fromisoformat(ts).timestamp()
                except Exception:
                    ts = 0.0
            if vin and st:
                self._raw_events[session_id].append({"vin": vin, "station_id": st, "timestamp": float(ts)})

    def run_discovery(self, session_id: str) -> Optional[DiscoverySession]:
        if session_id not in self._sessions:
            return None
        session = self._sessions[session_id]
        raw = self._raw_events.get(session_id, [])

        if not raw:
            session.status = "COMPLETED"
            return session

        # 1. Infer topology sequence
        top = TopologyInferenceEngine.infer_sequence(raw)
        session.inferred_topology = top

        # 2. Estimate takt time
        timestamps = [r["timestamp"] for r in raw]
        session.estimated_takt_time = TaktEstimator.estimate_takt(timestamps)

        # 3. Infer buffers
        session.inferred_buffers = BufferInferenceEngine.infer_buffers(
            station_sequence=top.station_sequence,
            unit_exit_events=raw,
            nominal_cycle_time=session.estimated_takt_time,
        )

        # 4. Detect parallel paths
        session.inferred_parallel_groups = ParallelPathDetector.detect_parallel_stations(raw)

        session.status = "COMPLETED"
        session.updated_at = datetime.now(timezone.utc)
        return session

    def get_session(self, session_id: str) -> Optional[DiscoverySession]:
        return self._sessions.get(session_id)
