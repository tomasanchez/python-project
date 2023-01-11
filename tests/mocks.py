"""
This module describes all shared mocks.
"""
from allocation.adapters.repository import SqlAlchemyRepository
from allocation.entrypoints.dependencies import get_batch_repository, get_session
from allocation.main import app


def override_session(session):
    """
    Overrides the session dependency for the FastAPI application.

    Args:
        session: a test SQLAlchemy session
    """
    app.dependency_overrides[get_session] = lambda: session


def override_batch_repository(repository: SqlAlchemyRepository):
    """
    Overrides the batch repository dependency for the FastAPI application.

    Args:
        repository: a Batch repository
    """
    app.dependency_overrides[get_batch_repository] = lambda: repository
