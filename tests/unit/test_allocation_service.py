"""
This module contains Allocation Service unit test cases.
"""
import pytest

from allocation.domain.models import Batch, OrderLine
from allocation.service_layer.allocation_service import AllocationService, InvalidSku, NoBatchesAvailable, OutOfStock
from tests.mocks import FakeRepository, FakeSession


class TestAllocationService:
    """
    Unit test suite for the allocation service layer
    """

    def test_returns_allocation(self):
        """
        Test that the allocation service returns an allocation.
        """
        line = OrderLine("o1", "COMPLICATED-LAMP", 10)
        batch = Batch("b1", "COMPLICATED-LAMP", 100, eta=None)
        repo = FakeRepository(Batch, [batch])

        result = self.get_service(repo).allocate(line)

        assert result == batch.reference

    def test_error_invalid_sku(self):
        """
        Test that the allocation service raises an error when an invalid SKU is provided.
        """
        line = OrderLine("o1", "NON-EXISTENT-SKU", 10)
        batch = Batch("b1", "A-REAL-SKU", 100, eta=None)
        repo = FakeRepository(Batch, [batch])

        with pytest.raises(InvalidSku, match="Invalid SKU"):
            self.get_service(repo).allocate(line)

    def test_error_no_batches(self):
        """
        Test that the allocation service raises an error when there are no batches available.
        """
        line = OrderLine("o1", "A-REAL-SKU", 10)
        repo = FakeRepository(Batch, [])

        with pytest.raises(NoBatchesAvailable, match="No batches available"):
            self.get_service(repo).allocate(line)

    def test_out_of_stock(self):
        """
        Test that the allocation service raises an error when there is no stock available.
        """
        line = OrderLine("o1", "A-REAL-SKU", 10)
        batch = Batch("b1", "A-REAL-SKU", 9, eta=None)
        repo = FakeRepository(Batch, [batch])

        with pytest.raises(OutOfStock, match="Out of stock"):
            self.get_service(repo).allocate(line)

    def test_does_commit(self):
        """
        Tests that the allocation service commits the session.
        """
        line = OrderLine("o1", "OMINOUS-MIRROR", 10)
        batch = Batch("b1", "OMINOUS-MIRROR", 100, eta=None)
        repo = FakeRepository(Batch, [batch])
        session = FakeSession()

        self.get_service(repo, session).allocate(line)

        assert session.committed is True

    @staticmethod
    def get_service(repository, session=FakeSession()):
        """
        Builds an Allocation service with a fake session

        Args:
            repository: a Fake repository
            session: a Fake session

        Returns:
            AllocationService: a spied AllocationService
        """
        return AllocationService(repository, session)
