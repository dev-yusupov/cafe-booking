from django.test import TestCase, Client
from django.urls import reverse
from cafe.models import Order


class OrderViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.order = Order.objects.create(
            table_number=1,
            items=[{'name': 'Coffee', 'quantity': 2, 'price': 3.5}],
            status=Order.STATUS_PENDING
        )

    def test_order_list_view(self):
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe/order.html')
        self.assertContains(response, self.order.id)

    def test_order_detail_view(self):
        response = self.client.get(reverse('order_detail', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe/order_detail.html')
        self.assertContains(response, self.order.id)

    def test_order_create_view(self):
        data = {
            'table_number': 2,
            'items': [{'name': 'Tea', 'quantity': 1, 'price': 2.0}]
        }
        response = self.client.post(reverse('order_create'), data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 2)

    def test_order_update_status_view(self):
        data = {'status': Order.STATUS_READY}
        response = self.client.post(reverse('order_update_status', args=[self.order.id]), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.STATUS_READY)
