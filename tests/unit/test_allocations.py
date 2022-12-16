"""
Allocation Tests.
"""

from datetime import date
from unittest import TestCase

from allocation.domain.models import Batch, OrderLine


def make_batch_and_line(sku, batch_qty, line_qty) -> tuple[Batch, OrderLine]:
    """
    Creates a batch and an order line with the given quantities.

    Args:
        sku (str): The sku of the batch and the line.
        batch_qty (int): The quantity of the batch.
        line_qty (int): The quantity of the line.

    Returns:
        tuple: A tuple containing the batch and the line.
    """
    return (
        Batch(ref='batch1',
              sku=sku, qty=batch_qty,
              eta=date.today()
              ),
        OrderLine(order_id='order1',
                  sku=sku,
                  qty=line_qty
                  ),
    )


class TestAllocationDomain(TestCase):
    """
    Allocation Domain Test Suite
    """

    def test_allocating_to_a_batch_reduces_tha_available_quantity(self):
        """
        Allocating to a batch reduces the available quantity.
        """
        batch, line = make_batch_and_line('SMALL-TABLE', 20, 2)

        batch.allocate(line)

        assert batch.available_quantity == 18

    def test_can_allocate_if_available_greater_than_required(self):
        """
        Can allocate if available greater than required.
        """
        large_batch, small_line = make_batch_and_line('ELEGANT-LAMP', 20, 2)

        assert large_batch.can_allocate(small_line)

    def test_cannot_allocate_if_available_smaller_than_required(self):
        """
        Cannot allocate if available smaller than required.
        """
        small_batch, large_line = make_batch_and_line('ELEGANT-LAMP', 2, 20)

        assert small_batch.can_allocate(large_line) is False

    def test_can_allocate_if_available_equal_to_required(self):
        """
        Can allocate if available equal to required.
        """
        batch, line = make_batch_and_line('ELEGANT-LAMP', 2, 2)

        assert batch.can_allocate(line)

    def test_cannot_allocate_if_skus_do_not_match(self):
        """
        Cannot allocate if skus do not match.
        """
        batch = Batch('batch1', 'UNCOMFORTABLE-CHAIR', 100, eta=None)
        different_sku_line = OrderLine('order1', 'EXPENSIVE-TOASTER', 10)

        assert batch.can_allocate(different_sku_line) is False

    def test_can_only_deallocate_allocated_lines(self):
        """
        Can only deallocate allocated lines.
        """
        batch, unallocated_line = make_batch_and_line('DECORATIVE-TRINKET', 20, 2)

        batch.deallocate(unallocated_line)

        assert batch.available_quantity == 20

    def test_allocation_is_idempotent(self):
        """
        Allocation is idempotent.
        """
        batch, line = make_batch_and_line('ANGULAR-DESK', 20, 2)

        batch.allocate(line)
        batch.allocate(line)

        assert batch.available_quantity == 18
