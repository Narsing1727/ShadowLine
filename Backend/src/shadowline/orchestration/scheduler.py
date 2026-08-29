"""Periodic background scheduler driving the twin forecast cycle."""

import asyncio
import logging
from typing import Optional
from shadowline.orchestration.prediction_cycle import PredictionCycleRunner

logger = logging.getLogger("shadowline.orchestration.scheduler")


class CycleScheduler:
    """Runs the prediction cycle on a recurring interval."""

    def __init__(self, runner: PredictionCycleRunner, interval_seconds: float = 60.0):
        self.runner = runner
        self.interval_seconds = max(1.0, interval_seconds)
        self.is_running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        self.is_running = True
        self._task = asyncio.create_task(self._loop())
        logger.info("Cycle scheduler started (interval=%.1fs)", self.interval_seconds)

    async def stop(self) -> None:
        self.is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Cycle scheduler stopped.")

    async def _loop(self) -> None:
        while self.is_running:
            try:
                # Run synchronous forecast cycle in threadpool to keep event loop responsive
                await asyncio.to_thread(self.runner.run_cycle)
            except Exception as e:
                logger.error("Error executing scheduled prediction cycle: %s", e)

            await asyncio.sleep(self.interval_seconds)
