from django.urls import path

from app_orders.api.views import OrdersView, OrderView, OrderCountView, CompletedOrderView

urlpatterns = [
    path('api/orders/', OrdersView.as_view(), name='orders'),
    path('api/orders/<int:id>/', OrderView.as_view(), name='order'),
    path('api/order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order_count_view'),
    path('api/completed-order-count/<int:business_user_id>/', CompletedOrderView.as_view(), name='completed_order_view'),
]