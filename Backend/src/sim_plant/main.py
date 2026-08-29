"""Simulated plant runner and entry point."""

import asyncio
from datetime import datetime, timezone
import logging
from typing import Optional
import simpy

from sim_plant.clock import SimClock
from sim_plant.config import SimPlantSettings, load_yaml
from sim_plant.emit.event_stream import SimEventStream
from sim_plant.emit.transport import get_global_transport
from sim_plant.faults.injector import FaultInjector
from sim_plant.model.line import SimLine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [sim_plant] %(message)s")
logger = logging.getLogger("sim_plant")


class SimPlantRunner:
    def __init__(self, settings: Optional[SimPlantSettings] = None):
        self.settings = settings or SimPlantSettings()
        self.line_config = load_yaml(self.settings.line_config)
        self.variants_config = load_yaml(self.settings.variants_config)
        self.faults_config = load_yaml(self.settings.faults_config)

        self.clock = SimClock(speed_factor=self.settings.speed_factor)
        self.transport = get_global_transport()
        self.event_stream = SimEventStream(
            clock=self.clock,
            sink=lambda evt: self.transport.publish_sync(evt),
        )

        self.env = simpy.Environment()
        self.line = SimLine(
            env=self.env,
            line_config=self.line_config,
            variants_config=self.variants_config,
            emit_callback=lambda evt_type, payload: self.event_stream.emit(
                evt_type, self.env.now, payload
            ),
        )
        self.injector = FaultInjector(
            env=self.env,
            stations=self.line.stations,
            faults_config=self.faults_config,
        )
        self.injector.schedule_all()

    def run_until(self, until_sim_seconds: float):
        logger.info("Running sim_plant until sim_seconds=%.1f", until_sim_seconds)
        self.env.run(until=until_sim_seconds)
        logger.info("sim_plant completed. Emitted %d events.", len(self.event_stream.emitted_events))

    async def run_realtime(self, duration_hours: float = 8.0):
        total_seconds = duration_hours * 3600.0
        step_seconds = 1.0
        logger.info("Starting real-time sim_plant execution (speed_factor=%.2f)...", self.settings.speed_factor)
        sim_time = 0.0
        while sim_time < total_seconds:
            self.env.run(until=sim_time + step_seconds)
            sim_time += step_seconds
            # Sleep proportionally to speed factor
            sleep_duration = step_seconds / self.settings.speed_factor
            await asyncio.sleep(min(1.0, sleep_duration))


def main():
    runner = SimPlantRunner()
    # Run 4 hours of simulation in batch mode if executed directly
    runner.run_until(4 * 3600.0)


if __name__ == "__main__":
    main()
