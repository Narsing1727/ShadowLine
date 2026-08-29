"""Pytest fixtures and test configuration."""

from datetime import datetime, timezone
import pytest
from httpx import ASGITransport, AsyncClient

from shadowline.api.app import create_app
from shadowline.config.line_loader import LineLoader
from shadowline.config.settings import ShadowLineSettings
from shadowline.domain.buffer import Buffer
from shadowline.domain.enums import ConfidenceTier, StationState, Zone
from shadowline.domain.station import Station
from shadowline.domain.topology import Topology
from shadowline.twin.snapshot import BufferSnapshot, StationSnapshot, TwinSnapshot, UnitSnapshot
from shadowline.twin.state_store import StateStore


@pytest.fixture
def sample_topology() -> Topology:
    stations = {
        "S-01": Station("S-01", "Station 1", Zone.BODY_SHOP, ConfidenceTier.MEASURED, 55.0),
        "S-02": Station("S-02", "Station 2", Zone.BODY_SHOP, ConfidenceTier.MEASURED, 58.0),
        "S-03": Station("S-03", "Station 3", Zone.PAINT_SHOP, ConfidenceTier.INFERRED, 54.0),
        "S-04": Station("S-04", "Station 4", Zone.FINAL_ASSEMBLY, ConfidenceTier.DARK, 52.0),
    }
    buffers = {
        "B-01": Buffer("B-01", "S-01", "S-02", capacity=3),
        "B-02": Buffer("B-02", "S-02", "S-03", capacity=4),
        "B-03": Buffer("B-03", "S-03", "S-04", capacity=3),
    }
    return Topology(
        line_id="test_line",
        name="Test Line",
        takt_time_seconds=58.0,
        target_jph=60.0,
        shifts_per_day=2,
        hours_per_shift=8.0,
        stations=stations,
        buffers=buffers,
        station_sequence=["S-01", "S-02", "S-03", "S-04"],
    )


@pytest.fixture
def sample_snapshot() -> TwinSnapshot:
    now = datetime.now(timezone.utc)
    stations = {
        "S-01": StationSnapshot("S-01", "Station 1", "BODY_SHOP", "MEASURED", 55.0, "ACTIVE", "VIN-001", 54.0, 300.0, 20.0, 10.0, 0.0, 10),
        "S-02": StationSnapshot("S-02", "Station 2", "BODY_SHOP", "MEASURED", 58.0, "ACTIVE", "VIN-002", 59.0, 450.0, 10.0, 10.0, 0.0, 8),
        "S-03": StationSnapshot("S-03", "Station 3", "PAINT_SHOP", "INFERRED", 54.0, "IDLE", None, 53.0, 200.0, 40.0, 50.0, 0.0, 7),
        "S-04": StationSnapshot("S-04", "Station 4", "FINAL_ASSEMBLY", "DARK", 52.0, "IDLE", None, None, 180.0, 0.0, 80.0, 0.0, 7),
    }
    buffers = {
        "B-01": BufferSnapshot("B-01", "S-01", "S-02", 3, 2, ["VIN-003", "VIN-004"]),
        "B-02": BufferSnapshot("B-02", "S-02", "S-03", 4, 1, ["VIN-005"]),
        "B-03": BufferSnapshot("B-03", "S-03", "S-04", 3, 0, []),
    }
    units = {
        "VIN-001": UnitSnapshot("VIN-001", "SUV_A", now.isoformat(), "S-01", []),
        "VIN-002": UnitSnapshot("VIN-002", "SEDAN_B", now.isoformat(), "S-02", ["D-WELD-01"]),
    }
    return TwinSnapshot(timestamp=now, stations=stations, buffers=buffers, in_flight_units=units)


@pytest.fixture
def state_store(sample_topology) -> StateStore:
    return StateStore(sample_topology)


@pytest.fixture
async def async_client():
    settings = ShadowLineSettings(mode="LIVE", db_url="sqlite:///:memory:")
    app = create_app(settings)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
