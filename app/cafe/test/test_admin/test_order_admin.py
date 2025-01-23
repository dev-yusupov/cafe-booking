from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from cafe.models import Order
from cafe.admin import OrderAdmin


class OrderAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.order_admin = OrderAdmin(Order, self.site)
        self.order = Order.objects.create(
            table_number=1,
            items=[{"name": "Coffee", "quantity": 2, "price": 5.00}],
            status=Order.STATUS_PENDING,
        )
        self.factory = RequestFactory()

    def test_list_display(self):
        """
        Test the list display configuration.
        """
        self.assertEqual(
            self.order_admin.list_display,
            ("id", "table_number", "status", "total_price", "created_at", "view_items"),
        )

    def test_list_filter(self):
        """
        Test the list filter configuration.
        """
        self.assertEqual(
            self.order_admin.list_filter, ("status", "created_at", "updated_at")
        )

    def test_search_fields(self):
        """
        Test the search fields configuration.
        """
        self.assertEqual(self.order_admin.search_fields, ("id", "table_number"))

    def test_readonly_fields(self):
        """
        Test the readonly fields configuration.
        """
        self.assertEqual(
            self.order_admin.readonly_fields,
            ("total_price", "created_at", "updated_at"),
        )

    def test_view_items(self):
        """
        Test the view items method.
        """
        items_html = self.order_admin.view_items(self.order)
        self.assertIn("<table", items_html)
        self.assertIn("Coffee", items_html)

    def test_mark_as_paid(self):
        """
        Test the mark as paid action.
        """
        request = self.factory.get("/")
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        queryset = Order.objects.filter(id=self.order.id)
        self.order_admin.mark_as_paid(request, queryset)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.STATUS_PAID)

    def test_fieldsets(self):
        """
        Test the fieldsets configuration.
        """
        self.assertEqual(
            self.order_admin.fieldsets,
            (
                (None, {"fields": ("table_number", "status", "items", "total_price")}),
                ("Timestamps", {"fields": ("created_at", "updated_at")}),
            ),
        )
