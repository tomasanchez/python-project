"""
This module contains the FastAPI router dependencies which are injected.
"""
from sqlalchemy.orm import clear_mappers

from allocation.adapters import database
from allocation.adapters.orm import start_mappers
from allocation.adapters.repository import SqlAlchemyRepository
from allocation.domain import models
from allocation.service_layer.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork


def get_session():
    """
    Obtains a session for the used database.
    """
    start_mappers()
    yield database.SessionLocal()
    clear_mappers()


def get_batch_repository() -> SqlAlchemyRepository:
    """
    Returns the SqlAlchemy repository instance for batches.
    """
    session = next(get_session())
    return SqlAlchemyRepository(session=session, kind=models.Batch)


def get_uow() -> AbstractUnitOfWork:
    """
    Returns the Unit of Work instance.
    """
    return SqlAlchemyUnitOfWork()
