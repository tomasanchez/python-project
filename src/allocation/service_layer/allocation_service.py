"""
This module describes the service responsible for allocating orders.
"""
from sqlalchemy.orm import Session

from allocation.adapters.repository import AbstractRepository
from allocation.domain.models import Batch, OrderLine


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

    def __init__(self, batch_repository: AbstractRepository, session: Session):
        self.batch_repository = batch_repository
        self.session = session

    def allocate(self, order: OrderLine) -> str:
        """
        Allocates an order line.

        Args:
            order (OrderLine): The order line to allocate.

        Returns:
            str: The reference of the batch allocated.

        Raises:
            InvalidSku: Raised when the SKU is invalid.
            OutOfStock: Raised when there is no stock available.
        """
        batches: list[Batch] = self.batch_repository.find_all()

        if not batches:
            raise NoBatchesAvailable()

        if not is_valid_sku(order.sku, batches):
            raise InvalidSku(order.sku)

        batch_ref = allocate(order, batches)

        if not batch_ref:
            raise OutOfStock()

        self.session.commit()

        return batch_ref


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
