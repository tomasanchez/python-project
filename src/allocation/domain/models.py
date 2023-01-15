"""Models.
 This module contains the models used by the allocation service.
"""

from dataclasses import dataclass
from datetime import date


@dataclass(unsafe_hash=True)
class OrderLine:
    """
    Represents an item in an order.

    Attributes:
        order_id (str): The order ID.
        sku (str): The SKU.
        qty (int): The quantity.
    """

    order_id: str
    sku: str
    qty: int


class Batch:
    """
    Represents Batch of a Stock.

    Attributes:
        reference (str): The batch reference.
        sku (str): The SKU.
        eta (date): Estimated Time of Arrival.
    """

    def __init__(self, ref: str, sku: str, qty: int, eta: date | None = None):
        self.reference: str = ref
        self.sku: str = sku
        self.eta: date | None = eta
        self._purchased_quantity = qty
        self._allocations: set[OrderLine] = set()

    def allocate(self, line: OrderLine):
        """
        Reduces the available quantity by the quantity of the line.

        Args:
            line (OrderLine): The line to allocate.
        """
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        """
        Increases the available quantity by the quantity of the line.

        Args:
            line (OrderLine): The line to deallocate.
        """
        if line in self._allocations:
            self._allocations.remove(line)

    def can_allocate(self, line: OrderLine) -> bool:
        """
        Checks if the batch can allocate the line.

        Args:
            line (OrderLine): The line to allocate.

        Returns:
            bool: True if the batch can allocate the line.
        """
        return self.sku == line.sku and self.available_quantity >= line.qty

    @property
    def allocated_quantity(self) -> int:
        """
        Sums the quantities of the allocated lines.

        Returns:
            int: the quantity allocated.
        """
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        """
        Calculates the difference between purchased and allocated.

        Returns:
            int: the available quantity.
        """
        return self._purchased_quantity - self.allocated_quantity

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta
