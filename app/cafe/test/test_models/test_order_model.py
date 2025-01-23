from django.test import TestCase
from django.core.exceptions import ValidationError
from cafe.models import Order


class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            table_number=1,
            items=[{"name": "Coffee", "quantity": 2, "price": 5.00}],
            status=Order.STATUS_PENDING,
        )

    def test_order_creation(self):
        self.assertEqual(self.order.table_number, 1)
        self.assertEqual(self.order.total_price, 10.00)
        self.assertEqual(self.order.status, Order.STATUS_PENDING)

    def test_order_string_representation(self):
        self.assertEqual(
            str(self.order), f"Order {self.order.id} at table {self.order.table_number}"
        )

    def test_total_price_calculation(self):
        self.order.items = [{"name": "Tea", "quantity": 1, "price": 3.00}]
        self.order.save()
        self.assertEqual(self.order.total_price, 3.00)

    def test_table_number_cannot_be_negative(self):
        invalid_order = Order(
            table_number=-1,
            items=[{"name": "Coffee", "quantity": 2, "price": 5.00}],
            status=Order.STATUS_PENDING,
        )
        with self.assertRaises(ValidationError):
            invalid_order.full_clean()

    def test_total_price_with_empty_items(self):
        empty_order = Order.objects.create(
            table_number=2, items=[], status=Order.STATUS_PENDING
        )
        self.assertEqual(empty_order.total_price, 0.00)

    def test_total_price_with_multiple_items(self):
        multiple_items_order = Order.objects.create(
            table_number=3,
            items=[
                {"name": "Coffee", "quantity": 2, "price": 5.00},
                {"name": "Tea", "quantity": 1, "price": 3.00},
            ],
            status=Order.STATUS_PENDING,
        )
        self.assertEqual(multiple_items_order.total_price, 13.00)

    def test_update_order(self):
        self.order.table_number = 2
        self.order.items = [{"name": "Latte", "quantity": 1, "price": 4.00}]
        self.order.save()
        self.order.refresh_from_db()
        self.assertEqual(self.order.table_number, 2)
        self.assertEqual(self.order.total_price, 4.00)

    def test_delete_order(self):
        order_id = self.order.id
        self.order.delete()
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(id=order_id)

    def test_order_crud_operations(self):
        # Create
        new_order = Order.objects.create(
            table_number=4,
            items=[{"name": "Espresso", "quantity": 3, "price": 2.50}],
            status=Order.STATUS_PENDING,
        )
        self.assertEqual(new_order.table_number, 4)
        self.assertEqual(new_order.total_price, 7.50)

        # Read
        fetched_order = Order.objects.get(id=new_order.id)
        self.assertEqual(fetched_order.table_number, 4)
        self.assertEqual(fetched_order.total_price, 7.50)

        # Update
        fetched_order.status = Order.STATUS_READY
        fetched_order.save()
        fetched_order.refresh_from_db()
        self.assertEqual(fetched_order.status, Order.STATUS_READY)

        # Delete
        fetched_order.delete()
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(id=fetched_order.id)
