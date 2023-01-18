"""
This module describes the service responsible for allocating orders.
"""
from datetime import date

from allocation.domain.models import Batch, OrderLine
from allocation.service_layer.unit_of_work import AbstractUnitOfWork


class InvalidSku(Exception):
    """
    Raised when an invalid SKU is provided.
    """

    def __init__(
        self,
        sku: str,
        message: str = "Invalid SKU",
    ):
        self.message = message
        self.sku = sku
        super().__init__(self.message)


class OutOfStock(Exception):
    """
    Raised when there is no stock available.
    """

    def __init__(self):
        self.message = "Out of stock"
        super().__init__(self.message)


class NoBatchesAvailable(Exception):
    """
    Raised when there are no batches available.
    """

    def __init__(self):
        self.message = "No batches available"
        super().__init__(self.message)


class AllocationService:
    """
    Abstraction responsible for allocating orders.
    """

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def allocate(self, order_id: str, sku: str, qty: int) -> str:
        """
        Allocates an order line.

        Args:
            order_id: Identifier of an order line
            sku: The Stock Keeping Unit
            qty: Quantity of the order line

        Returns:
            str: The reference of the batch allocated.

        Raises:
            NoBatchesAvailable: Raised when there are no batches available.
            InvalidSku: Raised when the SKU is invalid.
            OutOfStock: Raised when there is no stock available.
        """
        line = OrderLine(order_id=order_id, sku=sku, qty=qty)

        with self.uow:
            batches: list[Batch] = self.uow.batches.find_all()

            if not batches:
                raise NoBatchesAvailable()

            if not is_valid_sku(sku, batches):
                raise InvalidSku(sku)

            batch_ref = allocate(line, batches)

            if batch_ref is None:
                raise OutOfStock()

            self.uow.commit()

        return batch_ref

    def add_batch(self, ref: str, sku: str, qty: int, eta: date | None = None):
        """
        Adds a batch.

        Args:
            ref: The batch reference.
            sku: The Stock Keeping Unit
            qty: Quantity of the batch
            eta: Estimated time of arrival
        """
        with self.uow:
            self.uow.batches.save(Batch(ref=ref, sku=sku, qty=qty, eta=eta))
            self.uow.commit()


def allocate(order: OrderLine, batches: list[Batch]) -> str | None:
    """
    Allocates an order line in the oldest batch.

    Args:
        order: The order line to allocate.
        batches: a set of batches.

    Returns:
        str: The reference of the batch allocated.
    """

    # Sorted by ETA
    batches.sort()

    for batch in batches:
        if batch.can_allocate(order):
            batch.allocate(order)
            return batch.reference

    return None


def is_valid_sku(sku: str, batches: list[Batch]) -> bool:
    """
    Checks if the SKU is valid.

    Args:
        sku: The SKU to check.
        batches: a set of batches.

    Returns:
        bool: True if the SKU is valid, False otherwise.
    """
    return sku in {b.sku for b in batches}
