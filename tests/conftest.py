"""
This module contains pytest fixtures.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from allocation.orm import metadata, start_mappers


@pytest.fixture(name="in_memory_db")
def fixture_in_memory_db():
    """
    Creates an in-memory SQLite database.

    Returns:
        sqlalchemy.engine.Engine: An ORM engine for the in-memory DB.
    """
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
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
