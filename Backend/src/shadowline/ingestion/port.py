"""Abstract Ingestion Port interface.

Architectural Rule (Constraint 1): Read-only, always.
Software is never allowed to write to PLCs or control equipment.
This interface exposes ONLY read/streaming paths. No write/command methods exist.
"""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any, Optional
from shadowline.domain.events import CanonicalEvent


class IngestionPort(ABC):
    """Abstract read-only ingestion interface."""

    @abstractmethod
    async def start(self) -> None:
        """Starts the ingestion adapter."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stops the ingestion adapter gracefully."""
        pass

    @abstractmethod
    async def stream_events(self) -> AsyncGenerator[CanonicalEvent, None]:
        """Asynchronously streams normalized canonical events."""
        pass

    @abstractmethod
    async def get_health(self) -> Dict[str, Any]:
        """Returns the health status and statistics of the adapter."""
        pass
