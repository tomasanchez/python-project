"""
This module describes all shared mocks.
"""
import datetime
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from allocation.adapters.repository import AbstractRepository
from allocation.domain import models
from allocation.main import app
from allocation.service_layer.dependencies import get_uow
from allocation.service_layer.unit_of_work import AbstractUnitOfWork

T = TypeVar("T")


def override_uow(uow: AbstractUnitOfWork):
    """
    Overrides the UOW dependency for the FastAPI application.

    Args:
        uow: a Unit of Work
    """
    app.dependency_overrides[get_uow] = lambda: uow


class FakeRepository(AbstractRepository, Generic[T]):
    """
    A Fake Repository implementation
    """

    def __init__(self, kind: T, data: list[T] | None = None):
        if data is None:
            data = []

        self.data = data
        super().__init__(kind)

    def save(self, entity: T) -> None:
        self.data.append(entity)

    def find_by_id(self, entity_id: int) -> T:
        return next((x for x in self.data if x.id == entity_id), None)

    def find_all(self) -> list[T]:
        return self.data

    def find_by(self, **kwargs) -> T | None:
        return next((x for x in self.data if x.__dict__ == kwargs), None)

    def add(self, ref: str, sku: str, qty: int, eta: datetime.date | None = None):
        """
        Adds a batch.

        Args:
            ref: The batch reference.
            sku: The Stock Keeping Unit
            qty: Quantity
            eta: Estimated Time of Arrival

        """
        self.data.append(models.Batch(ref, sku, qty, eta))


class FakeSession(Session):
    """
    A mock session implementation.
    """

    committed = False

    def commit(self):
        """
        Mocks a commit in a session
        """
        self.committed = True

    def rollback(self) -> None:
        """
        Mocks a rollback in a session
        """
        self.committed = False


class FakeUoW(AbstractUnitOfWork):
    """
    A mock unit of work implementation.
    """

    def __init__(self, batches: AbstractRepository = None):
        if batches is None:
            batches = FakeRepository(models.Batch)

        self.batches = batches
        self.committed = False

    def commit(self):
        """
        Mocks a commit in a unit of work.
        """
        self.committed = True

    def rollback(self):
        """
        Mocks a rollback in a unit of work.
        """
        self.committed = False

    def __exit__(self, *args):
        pass

    def __enter__(self):
        return self
