"""SQLAlchemy database engine and session factory."""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

_engine = None
_SessionLocal = None


def get_db_engine(db_url: str = "sqlite:///./data/shadowline.db"):
    global _engine, _SessionLocal
    if _engine is None:
        # Ensure data folder exists
        if db_url.startswith("sqlite:///"):
            path_str = db_url.replace("sqlite:///", "")
            if path_str.startswith("./"):
                path_str = path_str[2:]
            db_path = Path(path_str).resolve()
            db_path.parent.mkdir(parents=True, exist_ok=True)

        _engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False} if db_url.startswith("sqlite") else {},
            echo=False,
        )
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    return _engine


def get_db_session(db_url: str = "sqlite:///./data/shadowline.db"):
    get_db_engine(db_url)
    session = _SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db(db_url: str = "sqlite:///./data/shadowline.db") -> None:
    engine = get_db_engine(db_url)
    Base.metadata.create_all(bind=engine)
