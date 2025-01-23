from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cafe.models import Order


class OrderAPITests(APITestCase):
    def setUp(self):
        self.order_data = {
            "table_number": 1,
            "items": [
                {"name": "Coffee", "price": 3.5, "quantity": 2},
                {"name": "Sandwich", "price": 5.0, "quantity": 1},
            ],
        }
        self.order = Order.objects.create(
            table_number=1, items=self.order_data["items"]
        )

    def test_create_order(self):
        url = reverse("order-list")
        response = self.client.post(url, self.order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

    def test_list_orders(self):
        url = reverse("order-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_order(self):
        url = reverse("order-detail", args=[self.order.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.order.id)

    def test_update_order(self):
        url = reverse("order-detail", args=[self.order.id])
        updated_data = self.order_data.copy()
        updated_data["status"] = Order.STATUS_READY
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.STATUS_READY)

    def test_delete_order(self):
        url = reverse("order-detail", args=[self.order.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
