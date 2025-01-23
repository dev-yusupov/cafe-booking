from django.urls import path, include

from rest_framework.routers import DefaultRouter

from cafe.views import (
    OrderView,
    OrderDetailView,
    OrderUpdateStatusView,
    OrderDeleteView,
    OrderViewSet,
    RevenueView,
)

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns: list = [
    path("orders/", OrderView.as_view(), name="order_list"),
    path("orders/create/", OrderView.as_view(), name="order_create"),
    path("orders/<int:order_id>/", OrderDetailView.as_view(), name="order_detail"),
    path(
        "orders/<int:order_id>/update_status/",
        OrderUpdateStatusView.as_view(),
        name="order_update_status",
    ),
    path(
        "orders/<int:order_id>/delete/", OrderDeleteView.as_view(), name="order_delete"
    ),
    path("api/v1/", include(router.urls)),
    path("revenue/", RevenueView.as_view(), name="revenue"),
]
