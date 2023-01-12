"""
This module test the FastAPI API.
"""
import uuid

from allocation.service_layer.allocation_service import InvalidSku, NoBatchesAvailable, OutOfStock
from tests.mocks import override_batch_repository, override_session


def random_sku():
    """
    Generate a random SKU.
    """
    return str(uuid.uuid4())


def random_batch_ref(param: int | None) -> str:
    """
    Generates a random batch reference.

    Args:
        param: a value

    Returns:
        str: A random UUID.
    """
    if param is None:
        return str(uuid.uuid4())
    else:
        return str(param)


def random_orderid():
    """
    Generates a random order ID.
    Returns:
        str: A random UUID.
    """
    return str(uuid.uuid4())


class TestAPI:
    """
    API end-to-end test cases.
    """

    def test_api_root_redirects_to_docs(self, test_client):
        """
        Tests that the root path redirects to the docs.
        """
        response = test_client.get("/").history[0]
        assert response.status_code == 301
        assert response.headers["location"] == "/docs"

    def test_api_returns_allocation(self, test_client, session, batch_repository, add_stock):
        """
        Tests that the API returns an allocation.
        """
        self.override_dependencies(session, batch_repository)

        sku, other_sku = random_sku(), random_sku()
        early_batch, later_batch, other_batch = random_batch_ref(1), random_batch_ref(2), random_batch_ref(3)

        add_stock(
            [
                (later_batch, sku, 100, "2011-01-02"),
                (early_batch, sku, 100, "2011-01-01"),
                (other_batch, other_sku, 100, None),
            ]
        )

        data = {"order_id": random_orderid(), "sku": sku, "qty": 3}
        r = test_client.post("/api/v1/allocate", json=data)

        assert r.status_code == 201
        assert r.json() == {"reference": early_batch}

    def test_api_no_batches(self, test_client, session, batch_repository):
        """
        Tests that the API returns a 404 when there are no batches.
        """
        self.override_dependencies(session, batch_repository)

        sku = random_sku()
        data = {"order_id": random_orderid(), "sku": sku, "qty": 3}

        r = test_client.post("/api/v1/allocate", json=data)

        assert r.status_code == 404
        assert r.json()["detail"] == NoBatchesAvailable().message

    def test_api_invalid_sku(self, test_client, session, batch_repository, add_stock):
        """
        Tests that the API returns a 400 when there is an invalid SKU, and there are batches.
        """
        self.override_dependencies(session, batch_repository)

        unknown_sku, known_sku = random_sku(), random_sku()

        add_stock([(random_batch_ref(None), known_sku, 100, None)])

        data = {"order_id": random_orderid(), "sku": unknown_sku, "qty": 20}
        r = test_client.post("/api/v1/allocate", json=data)
        assert r.status_code == 400
        assert r.json()["detail"] == InvalidSku(unknown_sku).message

    def test_api_out_of_stock(self, test_client, session, batch_repository, add_stock):
        """
        Tests that the API returns a 400 when there is an out-of-stock error, and there are batches.
        """
        self.override_dependencies(session, batch_repository)

        sku = random_sku()

        add_stock([(random_batch_ref(None), sku, 10, None)])

        data = {"order_id": random_orderid(), "sku": sku, "qty": 20}
        r = test_client.post("/api/v1/allocate", json=data)
        assert r.status_code == 400
        assert r.json()["detail"] == OutOfStock().message

    @staticmethod
    def override_dependencies(session, repository):
        """
        Overrides the Fast API dependencies.
        """
        override_batch_repository(repository)
        override_session(session)
