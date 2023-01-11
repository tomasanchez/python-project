"""
This module contains the FastAPI router dependencies which are injected.
"""
from sqlalchemy.orm import clear_mappers

from allocation import database
from allocation.adapters.orm import metadata, start_mappers
from allocation.adapters.repository import SqlAlchemyRepository
from allocation.domain import models


def get_session():
    """
    Obtains a session for the used database.
    """
    metadata.create_all(database.engine)

    start_mappers()
    yield database.SessionLocal()
    clear_mappers()


def get_batch_repository() -> SqlAlchemyRepository:
    """
    Returns the SqlAlchemy repository instance for batches.
    """
    session = next(get_session())
    return SqlAlchemyRepository(session=session, kind=models.Batch)
