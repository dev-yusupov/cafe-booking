from django.test import TestCase
from django.core.exceptions import ValidationError
from cafe.models import Order


class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            table_number=1,
            items=[{'name': 'Coffee', 'quantity': 2, 'price': 5.00}],
            status=Order.STATUS_PENDING
        )

    def test_order_creation(self):
        self.assertEqual(self.order.table_number, 1)
        self.assertEqual(self.order.total_price, 10.00)
        self.assertEqual(self.order.status, Order.STATUS_PENDING)

    def test_order_str(self):
        self.assertEqual(str(self.order), f"Order {self.order.id} at table {self.order.table_number}")

    def test_total_price_calculation(self):
        self.order.items = [{'name': 'Tea', 'quantity': 1, 'price': 3.00}]
        self.order.save()
        self.assertEqual(self.order.total_price, 3.00)

    def test_negative_table_number(self):
        order = Order(
            table_number=-1,
            items=[{'name': 'Coffee', 'quantity': 2, 'price': 5.00}],
            status=Order.STATUS_PENDING
        )
        with self.assertRaises(ValidationError):
            order.full_clean()

    def test_empty_items(self):
        order = Order.objects.create(
            table_number=2,
            items=[],
            status=Order.STATUS_PENDING
        )
        self.assertEqual(order.total_price, 0.00)

    def test_multiple_items(self):
        order = Order.objects.create(
            table_number=3,
            items=[
                {'name': 'Coffee', 'quantity': 2, 'price': 5.00},
                {'name': 'Tea', 'quantity': 1, 'price': 3.00}
            ],
            status=Order.STATUS_PENDING
        )
        self.assertEqual(order.total_price, 13.00)
