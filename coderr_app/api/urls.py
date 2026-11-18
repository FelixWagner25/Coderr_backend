from django.urls import path
from .views import OrderCompletedCountView, OrderCountView, OrderDetailView, OrderListCreateView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view()),
    path('orders/<int:id>/', OrderDetailView.as_view()),
    path('orders/order-count/<int:business_user_id>/', OrderCountView.as_view()),
    path('orders/completed_order-count/<int:business_user_id>/',
         OrderCompletedCountView.as_view())
]
