"""Replay a recorded or simulated shift through the digital twin."""

import asyncio
from datetime import datetime, timezone
import logging
from shadowline.config.line_loader import LineLoader
from shadowline.config.settings import ShadowLineSettings
from shadowline.domain.events import CanonicalEvent
from shadowline.orchestration.lifecycle import ServiceContainer
from sim_plant.main import SimPlantRunner

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [replay_shift] %(message)s")
logger = logging.getLogger("replay_shift")


async def replay_shift(duration_hours: float = 1.0, speed_multiplier: float = 100.0):
    logger.info("Setting up 1-shift replay simulation (duration=%.1fh, speed=%.1fx)...", duration_hours, speed_multiplier)

    # 1. Initialize sim_plant
    sim = SimPlantRunner()
    sim.run_until(duration_hours * 3600.0)
    raw_events = sim.event_stream.emitted_events

    logger.info("sim_plant generated %d events for shift replay.", len(raw_events))

    # 2. Ingest into shadowline
    container = ServiceContainer()
    for raw in raw_events:
        container.ingestion_adapter.inject_event(raw)

    # Process events into state store
    count = 0
    while not container.ingestion_adapter._queue.empty():
        evt = container.ingestion_adapter._queue.get_nowait()
        container.state_store.apply_event(evt)
        count += 1

    logger.info("Ingested and applied %d events to ShadowLine Digital Twin.", count)

    # 3. Run forecast cycle
    raw_preds, alerts, suppressed = container.cycle_runner.run_cycle()
    logger.info("Cycle results: %d predictions, %d alerts, %d suppressed.", len(raw_preds), len(alerts), len(suppressed))
    print("\n--- Shift Replay Summary ---")
    print(f"Total Events Processed: {container.state_store.total_events_processed}")
    print(f"Active In-Flight Units: {len(container.state_store.in_flight_units)}")
    print(f"Predictions Generated:  {len(raw_preds)}")
    print(f"Active Alerts:          {len(alerts)}")


if __name__ == "__main__":
    asyncio.run(replay_shift())
