"""Integration tests for all REST API endpoints verifying the API contract."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_api_contract_endpoints(async_client: AsyncClient):
    # 1. GET /health
    r = await async_client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "UP"

    # 2. GET /api/line
    r = await async_client.get("/api/line")
    assert r.status_code == 200
    assert "total_stations" in r.json()

    # 3. GET /api/line/state
    r = await async_client.get("/api/line/state")
    assert r.status_code == 200
    assert len(r.json()["stations"]) > 0

    # 4. GET /api/stations
    r = await async_client.get("/api/stations")
    assert r.status_code == 200
    stations = r.json()
    assert len(stations) > 0
    first_id = stations[0]["id"]

    # 5. GET /api/stations/{id}
    r = await async_client.get(f"/api/stations/{first_id}")
    assert r.status_code == 200
    assert r.json()["id"] == first_id

    # 6. GET /api/coverage
    r = await async_client.get("/api/coverage")
    assert r.status_code == 200
    assert "coverage_percentage" in r.json()

    # 7. GET /api/predictions/bottleneck
    r = await async_client.get("/api/predictions/bottleneck")
    assert r.status_code == 200
    assert "station_probabilities" in r.json()

    # 8. GET /api/defects/propagation
    r = await async_client.get("/api/defects/propagation")
    assert r.status_code == 200
    assert "nodes" in r.json()

    # 9. GET /api/trust/scorecard
    r = await async_client.get("/api/trust/scorecard")
    assert r.status_code == 200
    assert "precision" in r.json()

    # 10. GET /api/impact
    r = await async_client.get("/api/impact")
    assert r.status_code == 200
    assert "net_savings_usd" in r.json()

    # 11. GET /api/settings
    r = await async_client.get("/api/settings")
    assert r.status_code == 200
    assert "mode" in r.json()

    # 12. POST /api/discovery/session
    r = await async_client.post("/api/discovery/session", json={"line_name": "Discovery Test Line"})
    assert r.status_code == 200
    s_id = r.json()["session_id"]
    assert s_id is not None
