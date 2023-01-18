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

from allocation.adapters.orm import metadata, start_mappers
from allocation.main import app
from allocation.service_layer.unit_of_work import SqlAlchemyUnitOfWork


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


@pytest.fixture(name="session_factory")
def fixture_session_factory(in_memory_db) -> Callable:
    """
    Creates a session factory for the in-memory SQLite database.

    Parameters:
        in_memory_db (sqlalchemy.engine.Engine): The in-memory SQLite database.

    Returns:
        Callable: A session factory for the in-memory SQLite database.
    """
    start_mappers()
    yield partial(sessionmaker(bind=in_memory_db))
    clear_mappers()


@pytest.fixture
def uow(session_factory) -> SqlAlchemyUnitOfWork:
    """
    Provides a unit of work for the in-memory SQLite database.

    Args:
        session_factory: A session factory for the in-memory SQLite database.

    Returns:
        SqlAlchemyUnitOfWork: A unit of work for the in-memory SQLite database.
    """
    return SqlAlchemyUnitOfWork(session_factory=session_factory)
