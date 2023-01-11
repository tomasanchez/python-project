"""
This module contains pytest fixtures.
"""
from functools import partial
from typing import Callable

import pytest
import sqlalchemy.engine
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from allocation.domain.models import Batch
from allocation.main import app
from allocation.orm import metadata, start_mappers
from allocation.repository.repository import SqlAlchemyRepository


@pytest.fixture(name="test_client")
def fixture_test_client() -> TestClient:
    """
    Create a test client for the FastAPI application.

    Returns:
        TestClient: A test client for the app.
    """
    return TestClient(app)


@pytest.fixture(name="in_memory_db")
def fixture_in_memory_db() -> sqlalchemy.engine.Engine:
    """
    Creates an in-memory SQLite engine using a StaticPool.

    Returns:
        sqlalchemy.engine.Engine: An ORM engine for the in-memory DB.
    """
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def fixture_session(in_memory_db) -> sqlalchemy.orm.session.Session:
    """
    Creates a session for the in-memory SQLite database.

    Parameters:
        in_memory_db (sqlalchemy.engine.Engine): The in-memory SQLite database.

    Returns:
        sqlalchemy.orm.session.Session: The session for the in-memory SQLite database.
    """
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


@pytest.fixture
def add_stock(session) -> Callable[[list[tuple[str, str, int, str | None]]], None]:
    """
    Provides an easy way of persisting batches.

    Parameters:
        session (sqlalchemy.orm.session.Session): The session for the in-memory SQLite database.

    Returns: Callable[[list[tuple[str, str, int, str | None]]], None]: A function that given a list of batches,
    saves them to in-memory DB.
    """

    def add_to_db(_session, _batches):
        """
        Saves to the database.

        Args:
            _session: The session for the in-memory SQLite database.
            _batches (tuple): A list of batches.
        """
        _session.execute(
            "INSERT INTO batches (reference, sku, _purchased_quantity, eta) VALUES (:reference, :sku, :qty, :eta)",
            [
                {
                    "reference": reference,
                    "sku": sku,
                    "qty": qty,
                    "eta": eta,
                }
                for (reference, sku, qty, eta) in _batches
            ],
        )
        _session.commit()

    return partial(add_to_db, session)


@pytest.fixture
def batch_repository(session) -> SqlAlchemyRepository:
    """
    Provides a repository for batches.

    Args:
        session: the session for the in-memory SQLite database.

    Returns:
        SqlAlchemyRepository: a repository for batches.
    """
    return SqlAlchemyRepository(session=session, kind=Batch)
