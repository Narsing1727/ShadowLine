"""FastAPI dependency injection providers."""

from typing import Generator, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from shadowline.config.settings import ShadowLineSettings
from shadowline.orchestration.lifecycle import ServiceContainer
from shadowline.persistence.engine import get_db_session

# Global container reference assigned on app startup
_container: Optional[ServiceContainer] = None


def set_service_container(container: ServiceContainer) -> None:
    global _container
    _container = container


def get_service_container() -> ServiceContainer:
    if _container is None:
        raise RuntimeError("Service container is not initialized.")
    return _container


def get_db() -> Generator[Session, None, None]:
    container = get_service_container()
    yield from get_db_session(container.settings.db_url)
