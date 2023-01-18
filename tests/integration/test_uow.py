"""
Test Integration Suite for Unit of Work.
"""
import pytest

from allocation.domain.models import OrderLine
from allocation.service_layer.unit_of_work import SqlAlchemyUnitOfWork


def insert_batch(session, reference, sku: str, qty: int, eta: str | None):
    """
    Saves a batch to the database.

    Args:
        session: The SQLAlchemy session.
        reference: The batch reference.
        sku: The Stock Keeping Unit.
        qty: The quantity of the batch.
        eta: The Estimated Time of Arrival.
    """
    session.execute(
        """INSERT INTO batches (reference, sku, _purchased_quantity, eta)
         VALUES (:reference, :sku, :qty, :eta)
         """,
        dict(reference=reference, sku=sku, qty=qty, eta=eta),
    )


def get_allocated_batch_ref(session, order_id, sku) -> str | None:
    """
    Gets the allocated batch reference for an order.

    Args:
        session: The SQLAlchemy session.
        order_id: The order id.
        sku: The Stock Keeping Unit.

    Returns:
        str: The batch reference.
    """

    [[batch_ref]] = session.execute(
        """
        SELECT b.reference
        FROM allocations JOIN batches AS b ON b.id = allocations.batch_id
        WHERE orderline_id = (
            SELECT id FROM order_lines WHERE order_id = :order_id AND sku = :sku
        )
        """,
        dict(order_id=order_id, sku=sku),
    )
    return batch_ref


class TestUnitOfWork:
    """
    Unit of Work test cases.
    """

    def test_uow_can_retrieve_a_batch_and_allocate_to_it(self, session_factory):
        """
        Test that a batch can be retrieved from the database and allocated to.
        """

        session = session_factory()

        insert_batch(session, "batch1", "HIPSTER-WORKBENCH", 100, None)

        session.commit()

        uow = SqlAlchemyUnitOfWork(session_factory)

        with uow:
            batch = uow.batches.find_by(reference="batch1")
            line = OrderLine("o1", "HIPSTER-WORKBENCH", 10)
            batch.allocate(line)
            uow.commit()

        batch_ref = get_allocated_batch_ref(session, "o1", "HIPSTER-WORKBENCH")

        assert batch_ref == "batch1"

    def test_rolls_back_uncommitted_work_by_default(self, session_factory):
        """
        Test that uncommitted work is rolled back by default.
        """

        uow = SqlAlchemyUnitOfWork(session_factory)

        with uow:
            insert_batch(uow.session, "batch1", "GENERIC-SOFA", 100, None)

        rows = list(uow.session.execute("SELECT * FROM batches"))

        assert rows == []

    def test_rolls_back_on_error(self, session_factory):
        """
        Test that uncommitted work is rolled back on error.
        """

        class CustomException(Exception):
            """
            Custom exception.
            """

            pass

        uow = SqlAlchemyUnitOfWork(session_factory)

        with pytest.raises(CustomException):
            with uow:
                insert_batch(uow.session, "batch1", "GENERIC-SOFA", 100, None)
                raise CustomException()

        rows = list(uow.session.execute("SELECT * FROM batches"))

        assert rows == []
