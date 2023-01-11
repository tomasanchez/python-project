"""
Test Suites for the SQLAlchemy Repository.
"""
from allocation.adapters import repository
from allocation.domain import models


def insert_order_line(session) -> int:
    """
    Saves an order line to the database.

    Args:
        session: The SQLAlchemy session.

    Returns:
        int: The inserted order line id.

    """

    session.execute(  #
        "INSERT INTO order_lines (order_id, sku, qty) VALUES (:order_id, :sku, :qty)",
        dict(order_id="order1", sku="GENERIC-SOFA", qty=12),
    )

    [[order_line_id]] = session.execute(
        "SELECT id FROM order_lines WHERE order_id=:orderid AND sku=:sku",
        dict(orderid="order1", sku="GENERIC-SOFA"),
    )

    return order_line_id


def insert_batch(session, reference) -> int:
    """
    Saves a batch to the database.

    Args:
        session: The SQLAlchemy session.
        reference: The batch reference.

    Returns:
        int: The inserted batch id.

    """
    session.execute(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta)" "VALUES (:reference, :sku, :qty, :eta)",
        dict(reference=reference, sku="GENERIC-SOFA", qty=100, eta="2021-01-01"),
    )

    [[batch_id]] = session.execute(
        "SELECT id FROM batches WHERE reference=:reference AND sku=:sku",
        dict(reference=reference, sku="GENERIC-SOFA"),
    )

    return batch_id


def insert_allocation(session, order_id, batch_id) -> int:
    """
    Saves an allocation to the database.

    Args:
        session: The SQLAlchemy session.
        order_id: The order id.
        batch_id: The batch id.

    Returns:
        int: The inserted allocation id.
    """
    session.execute(
        "INSERT INTO allocations (orderline_id, batch_id)" "VALUES (:orderline_id, :batch_id)",
        dict(orderline_id=order_id, batch_id=batch_id),
    )

    [[allocation_id]] = session.execute(
        "SELECT id FROM allocations WHERE orderline_id=:orderline_id AND batch_id=:batch_id",
        dict(orderline_id=order_id, batch_id=batch_id),
    )

    return allocation_id


class TestRepository:
    def test_repository_can_retrieve_a_batch_with_allocations(self, session):
        order_line_id = insert_order_line(session)
        batch1_id = insert_batch(session, "batch1")
        insert_batch(session, "batch2")
        insert_allocation(session, order_line_id, batch1_id)

        repo = repository.SqlAlchemyRepository(session, kind=models.Batch)
        # noinspection PyTypeChecker
        retrieved: models.Batch = repo.find_by_id(batch1_id)

        expected = models.Batch("batch1", "GENERIC-SOFA", 100)
        assert retrieved == expected
        assert retrieved.sku == expected.sku
        assert retrieved._purchased_quantity == expected._purchased_quantity
        assert retrieved._allocations == {
            models.OrderLine("order1", "GENERIC-SOFA", 12),
        }
