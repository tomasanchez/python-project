"""
Test cases for the ORM  module.
"""
import allocation.domain.models as model


class TestORM:
    def test_order_line_mapper_can_load_lines(self, session):
        lines = [
            ("order1", "RED-CHAIR", 12),
            ("order2", "RED-TABLE", 13),
            ("order3", "BLUE-LIPSTICK", 14),
        ]

        session.execute(
            "INSERT INTO order_lines (order_id, sku, qty)" " VALUES (:order_id, :sku, :qty)",
            [
                {
                    "order_id": order_id,
                    "sku": sku,
                    "qty": qty,
                }
                for order_id, sku, qty in lines
            ],
        )

        expected = [model.OrderLine(order_id, sku, qty) for (order_id, sku, qty) in lines]

        assert session.query(model.OrderLine).all() == expected

    def test_order_line_mapper_can_save_lines(self, session):
        new_line = model.OrderLine("order1", "DECORATIVE-WIDGET", 12)
        session.add(new_line)
        session.commit()

        rows = list(session.execute('SELECT order_id, sku, qty FROM "order_lines"'))
        assert rows == [("order1", "DECORATIVE-WIDGET", 12)]

    def test_batch_mapper_can_load_batches(self, session):
        batches = [
            ("batch1", "RED-CHAIR", 100, None),
            ("batch2", "RED-CHAIR", 100, None),
            ("batch3", "BLUE-LIPSTICK", 100, None),
        ]

        session.execute(
            "INSERT INTO batches (reference, sku, _purchased_quantity, eta)" " VALUES (:reference, :sku, :qty, :eta)",
            [
                {
                    "reference": ref,
                    "sku": sku,
                    "qty": qty,
                    "eta": eta,
                }
                for ref, sku, qty, eta in batches
            ],
        )

        expected = [model.Batch(ref, sku, qty, eta) for (ref, sku, qty, eta) in batches]

        assert session.query(model.Batch).all() == expected

    def test_batch_mapper_can_save_batches(self, session):
        new_batch = model.Batch("batch1", "DECORATIVE-WIDGET", 100, None)
        session.add(new_batch)
        session.commit()

        rows = list(session.execute('SELECT reference, sku, _purchased_quantity, eta FROM "batches"'))
        assert rows == [("batch1", "DECORATIVE-WIDGET", 100, str(new_batch.eta))]

    def test_product_mapper_can_load_products(self, session):
        products = [
            "RED-CHAIR",
            "RED-TABLE",
            "BLUE-LIPSTICK",
        ]

        session.execute(
            "INSERT INTO products (sku)" " VALUES (:sku)",
            [
                {
                    "sku": sku,
                }
                for sku in products
            ],
        )

        expected = [model.Product(sku) for (sku) in products]

        assert session.query(model.Product).all() == expected

    def test_product_mapper_can_save_products(self, session):
        new_product = model.Product("DECORATIVE-WIDGET")
        session.add(new_product)
        session.commit()

        rows = list(session.execute('SELECT sku FROM "products"'))
        assert rows == [("DECORATIVE-WIDGET",)]

    def test_product_mapper_can_load_batches(self, session):
        product_sku = "RED-CHAIR"

        batches = [
            ("batch1", product_sku, 100, None),
            ("batch2", product_sku, 100, None),
            ("batch3", "BLUE-LIPSTICK", 100, None),
        ]

        session.execute(
            "INSERT INTO products (sku)" " VALUES (:sku)",
            [
                {
                    "sku": product_sku,
                }
            ],
        )

        session.execute(
            "INSERT INTO batches (reference, sku, _purchased_quantity, eta)" " VALUES (:reference, :sku, :qty, :eta)",
            [
                {
                    "reference": ref,
                    "sku": sku,
                    "qty": qty,
                    "eta": eta,
                }
                for ref, sku, qty, eta in batches
            ],
        )

        product = session.query(model.Product).filter_by(sku=product_sku).one()

        expected = [model.Batch(ref, sku, qty, eta) for (ref, sku, qty, eta) in batches if sku == product_sku]

        assert product.batches == expected

    def test_product_mapper_can_save_batches(self, session):
        # given
        product_sku = "DECORATIVE-WIDGET"

        new_product = model.Product(product_sku)
        new_batch = model.Batch("batch1", product_sku, 100, None)
        new_product.batches.append(new_batch)

        # when
        session.add(new_product)
        session.commit()
        rows = list(session.execute('SELECT sku, reference FROM "batches"'))

        # then
        assert rows == [(product_sku, "batch1")]
