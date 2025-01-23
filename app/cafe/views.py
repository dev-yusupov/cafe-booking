from django.views.generic import View, DeleteView, TemplateView
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django_filters.views import FilterView
from django_filters import rest_framework as filters

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, request, response
from rest_framework.pagination import PageNumberPagination

from typing import Optional, Dict, Any
import json

from .models import Order
from .serializers import OrderSerializer


class OrderFilter(filters.FilterSet):
    """
    FilterSet for filtering orders by table number and status.
    """

    table_number = filters.NumberFilter(field_name="table_number")
    status = filters.ChoiceFilter(choices=Order.STATUS_CHOICES)

    class Meta:
        model = Order
        fields = ["table_number", "status"]


class OrderView(FilterView):
    """
    View for displaying and filtering orders.
    """

    model = Order
    template_name = "cafe/order.html"
    context_object_name = "orders"
    filterset_class = OrderFilter

    def get_context_data(self, **kwargs):
        """
        Get the context data for the template.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset_class(
            self.request.GET, queryset=self.get_queryset()
        )
        context["query_params"] = self.request.GET.urlencode()
        return context

    def get_queryset(self):
        """
        Get the filtered queryset.

        Returns:
            QuerySet: The filtered queryset.
        """
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    @method_decorator(csrf_exempt)
    def post(self, request: HttpRequest) -> JsonResponse:
        """
        Handle POST requests to create a new order.

        Args:
            request (HttpRequest): The HTTP request.

        Returns:
            JsonResponse: The JSON response.
        """
        data: Dict[str, Any] = json.loads(request.body)
        table_number: Optional[int] = data.get("table_number")
        items: Optional[str] = data.get("items")

        if table_number and items:
            order: Order = Order.objects.create(table_number=table_number, items=items)
            return JsonResponse({"id": order.id, "status": "created"}, status=201)
        return JsonResponse({"error": "Invalid data"}, status=400)


class OrderDetailView(View):
    """
    View for displaying the details of a specific order.
    """

    def get(self, request: HttpRequest, order_id: int) -> HttpResponse:
        """
        Handle GET requests to display order details.

        Args:
            request (HttpRequest): The HTTP request.
            order_id (int): The ID of the order.

        Returns:
            HttpResponse: The HTTP response.
        """
        order: Optional[Order] = get_object_or_404(Order, id=order_id)
        return render(request, "cafe/order_detail.html", {"order": order})


class OrderUpdateStatusView(View):
    """
    View for updating the status of a specific order.
    """

    @method_decorator(csrf_exempt)
    def post(self, request: HttpRequest, order_id: int) -> JsonResponse:
        """
        Handle POST requests to update order status.

        Args:
            request (HttpRequest): The HTTP request.
            order_id (int): The ID of the order.

        Returns:
            JsonResponse: The JSON response.
        """
        order: Optional[Order] = get_object_or_404(Order, id=order_id)
        data: Dict[str, Any] = json.loads(request.body)
        status: Optional[str] = data.get("status")

        if status in [Order.STATUS_PENDING, Order.STATUS_READY, Order.STATUS_PAID]:
            order.status = status
            order.save()
            return JsonResponse({"status": "updated"}, status=200)
        return JsonResponse({"error": "Invalid status"}, status=400)


class OrderDeleteView(DeleteView):
    """
    View for deleting a specific order.
    """

    @method_decorator(csrf_exempt)
    def delete(self, request: HttpRequest, order_id: int) -> JsonResponse:
        """
        Handle DELETE requests to delete an order.

        Args:
            request (HttpRequest): The HTTP request.
            order_id (int): The ID of the order.

        Returns:
            JsonResponse: The JSON response.
        """
        order: Optional[Order] = get_object_or_404(Order, id=order_id)
        order.delete()
        return JsonResponse({"status": "deleted"}, status=204)


class RevenueView(TemplateView):
    """
    View for displaying the total revenue.
    """

    template_name = "cafe/revenue.html"

    def get_context_data(self, **kwargs):
        """
        Get the context data for the template.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        total_revenue = (
            Order.objects.filter(status=Order.STATUS_PAID).aggregate(
                Sum("total_price")
            )["total_price__sum"]
            or 0
        )
        context["total_revenue"] = total_revenue
        return context


class OrderPagination(PageNumberPagination):
    """
    Pagination class for orders.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class OrderViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    ViewSet for managing orders via the API.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination

    def create(self, request: request.Request, *args, **kwargs) -> response.Response:
        """
        Handle POST requests to create a new order.

        Args:
            request (request.Request): The HTTP request.

        Returns:
            response.Response: The HTTP response.
        """
        return super().create(request, *args, **kwargs)

    def list(self, request: request.Request, *args, **kwargs) -> response.Response:
        """
        Handle GET requests to list orders.

        Args:
            request (request.Request): The HTTP request.

        Returns:
            response.Response: The HTTP response.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request: request.Request, *args, **kwargs) -> response.Response:
        """
        Handle GET requests to retrieve a specific order.

        Args:
            request (request.Request): The HTTP request.

        Returns:
            response.Response: The HTTP response.
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request: request.Request, *args, **kwargs) -> response.Response:
        """
        Handle PUT requests to update a specific order.

        Args:
            request (request.Request): The HTTP request.

        Returns:
            response.Response: The HTTP response.
        """
        return super().update(request, *args, **kwargs)

    def destroy(self, request: request.Request, *args, **kwargs) -> response.Response:
        """
        Handle DELETE requests to delete a specific order.

        Args:
            request (request.Request): The HTTP request.

        Returns:
            response.Response: The HTTP response.
        """
        return super().destroy(request, *args, **kwargs)
