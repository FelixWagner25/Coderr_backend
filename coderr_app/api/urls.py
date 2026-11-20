from django.urls import path
from .views import OrderCompletedCountView, OrderCountView, OrderDetailView, OrderListCreateView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:business_user_id>/',
         OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/',
         OrderCompletedCountView.as_view(), name='completed-order-count')
]
