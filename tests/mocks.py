"""
This module describes all shared mocks.
"""
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from allocation.adapters.repository import AbstractRepository, SqlAlchemyRepository
from allocation.entrypoints.dependencies import get_batch_repository, get_session
from allocation.main import app

T = TypeVar("T")


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


class FakeRepository(AbstractRepository, Generic[T]):
    """
    A Fake Repository implementation
    """

    def __init__(self, kind: T, data: list[T]):
        self.data = data
        super().__init__(kind)

    def save(self, entity: T) -> None:
        self.data.append(entity)

    def find_by_id(self, entity_id: int) -> T:
        return next((x for x in self.data if x.id == entity_id), None)

    def find_all(self) -> list[T]:
        return self.data


class FakeSession(Session):
    committed = False

    def commit(self):
        """
        Mocks a commit in a session
        """
        self.committed = True
