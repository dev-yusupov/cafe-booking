from django.views.generic import View, DeleteView
from django.shortcuts import render, get_object_or_404
from .models import Order
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


class OrderView(View):
    def get(self, request):
        orders = Order.objects.all()
        return render(request, "cafe/order.html", {"orders": orders})

    @method_decorator(csrf_exempt)
    def post(self, request):
        data = json.loads(request.body)
        table_number = data.get('table_number')
        items = data.get('items')
        if table_number and items:
            order = Order.objects.create(table_number=table_number, items=items)
            return JsonResponse({'id': order.id, 'status': 'created'}, status=201)
        return JsonResponse({'error': 'Invalid data'}, status=400)


class OrderDetailView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, "cafe/order_detail.html", {"order": order})


class OrderUpdateStatusView(View):
    @method_decorator(csrf_exempt)
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        data = json.loads(request.body)
        status = data.get('status')
        if status in [Order.STATUS_PENDING, Order.STATUS_READY, Order.STATUS_PAID]:
            order.status = status
            order.save()
            return JsonResponse({'status': 'updated'}, status=200)
        return JsonResponse({'error': 'Invalid status'}, status=400)


class OrderDeleteView(DeleteView):
    @method_decorator(csrf_exempt)
    def delete(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        return JsonResponse({'status': 'deleted'}, status=204)
