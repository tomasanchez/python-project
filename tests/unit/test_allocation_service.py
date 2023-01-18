"""
This module contains Allocation Service unit test cases.
"""
import datetime

import pytest

from allocation.service_layer.allocation_service import AllocationService, InvalidSku, NoBatchesAvailable, OutOfStock
from allocation.service_layer.unit_of_work import AbstractUnitOfWork
from tests.mocks import FakeUoW


class TestAllocationService:
    """
    Unit test suite for the allocation service layer
    """

    def test_returns_allocation(self):
        """
        Test that the allocation service returns an allocation.
        """
        batch_ref = "b1"

        service = self.get_service()

        service.add_batch(batch_ref, "COMPLICATED-LAMP", 100, eta=None)

        result = service.allocate("o1", "COMPLICATED-LAMP", 10)

        assert result == batch_ref

    def test_error_invalid_sku(self):
        """
        Test that the allocation service raises an error when an invalid SKU is provided.
        """
        service = self.get_service()
        service.add_batch("b1", "A-REAL-SKU", 100, eta=None)

        with pytest.raises(InvalidSku, match="Invalid SKU"):
            service.allocate("o1", "NON-EXISTENT-SKU", 10)

    def test_error_no_batches(self):
        """
        Test that the allocation service raises an error when there are no batches available.
        """
        with pytest.raises(NoBatchesAvailable, match="No batches available"):
            self.get_service().allocate("o1", "A-REAL-SKU", 10)

    def test_out_of_stock(self):
        """
        Test that the allocation service raises an error when there is no stock available.
        """
        service = self.get_service()
        service.add_batch("b1", "A-REAL-SKU", 9, eta=None)

        with pytest.raises(OutOfStock, match="Out of stock"):
            service.allocate("o1", "A-REAL-SKU", 10)

    def test_does_commit(self):
        """
        Tests that the allocation service commits the session.
        """
        service = self.get_service()

        # noinspection PyTypeChecker
        uow: FakeUoW = service.uow

        service.add_batch("b1", "OMINOUS-MIRROR", 100, eta=None)

        service.allocate("o1", "OMINOUS-MIRROR", 10)

        assert uow.committed is True

    def test_prefer_warehouse_batches_to_shipments(self):
        """
        Tests that the allocation service prefers warehouse batches to shipments.
        """
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        service = self.get_service()
        in_stock_ref = "in-stock-batch"

        service.add_batch(in_stock_ref, "RETRO-CLOCK", 100, eta=None)
        service.add_batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)

        allocated_ref = service.allocate("o-ref", "RETRO-CLOCK", 10)

        assert allocated_ref == in_stock_ref

    @staticmethod
    def get_service(uow: AbstractUnitOfWork = None) -> AllocationService:
        """
        Builds an Allocation service with a fake session

        Args:
            uow: The unit of work to use

        Returns:
            AllocationService: a spied AllocationService
        """
        if uow is None:
            uow = FakeUoW()

        return AllocationService(uow)
