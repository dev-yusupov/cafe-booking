from django.views.generic import View, DeleteView
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models.query import QuerySet

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status, request, response

from typing import Optional, Dict, Any
import json

from .models import Order
from .serializers import OrderSerializer


class OrderView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        orders: QuerySet[Order] = Order.objects.all()
        return render(request, "cafe/order.html", {"orders": orders})

    @method_decorator(csrf_exempt)
    def post(self, request: HttpRequest) -> JsonResponse:
        data: Dict[str, Any] = json.loads(request.body)
        table_number: Optional[int] = data.get('table_number')
        items: Optional[str] = data.get('items')

        if table_number and items:
            order: Order = Order.objects.create(table_number=table_number, items=items)
            return JsonResponse({'id': order.id, 'status': 'created'}, status=201)
        return JsonResponse({'error': 'Invalid data'}, status=400)


class OrderDetailView(View):
    def get(self, request: HttpRequest, order_id: int) -> HttpResponse:
        order: Optional[Order] = get_object_or_404(Order, id=order_id)
        return render(request, "cafe/order_detail.html", {"order": order})


class OrderUpdateStatusView(View):
    @method_decorator(csrf_exempt)
    def post(self, request: HttpRequest, order_id: int) -> JsonResponse:
        order: Optional[Order] = get_object_or_404(Order, id=order_id)
        data: Dict[str, Any] = json.loads(request.body)
        status: Optional[str] = data.get('status')

        if status in [Order.STATUS_PENDING, Order.STATUS_READY, Order.STATUS_PAID]:
            order.status = status
            order.save()
            return JsonResponse({'status': 'updated'}, status=200)
        return JsonResponse({'error': 'Invalid status'}, status=400)


class OrderDeleteView(DeleteView):
    @method_decorator(csrf_exempt)
    def delete(self, request: HttpRequest, order_id: int) -> JsonResponse:
        order: Optional[Order] = get_object_or_404(Order, id=order_id)
        order.delete()
        return JsonResponse({'status': 'deleted'}, status=204)


class OrderViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request: request.Request, *args, **kwargs) -> response.Response:
        return super().create(request, *args, **kwargs)

    def list(self, request: request.Request, *args, **kwargs) -> response.Response:
        return super().list(request, *args, **kwargs)

    def retrieve(self, request: request.Request, *args, **kwargs) -> response.Response:
        return super().retrieve(request, *args, **kwargs)

    def update(self, request: request.Request, *args, **kwargs) -> response.Response:
        return super().update(request, *args, **kwargs)

    def destroy(self, request: request.Request, *args, **kwargs) -> response.Response:
        return super().destroy(request, *args, **kwargs)