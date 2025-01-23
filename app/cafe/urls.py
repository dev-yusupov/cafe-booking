from django.urls import path # noqa
from cafe.views import OrderView, OrderDetailView, OrderUpdateStatusView, OrderDeleteView, OrderViewSet

urlpatterns: list = [
    path('orders/', OrderView.as_view(), name='order_list'),
    path('orders/create/', OrderView.as_view(), name='order_create'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:order_id>/update_status/', OrderUpdateStatusView.as_view(), name='order_update_status'),
    path('orders/<int:order_id>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path("api/v1/orders/", OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='order_api'),
]
