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
