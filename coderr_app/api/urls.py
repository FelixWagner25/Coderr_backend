from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfferDetailView, OfferViewSet, OrderCompletedCountView, OrderCountView, OrderDetailView, OrderListCreateView, ReviewViewSet

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'offers', OfferViewSet, basename='offer')

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:business_user_id>/',
         OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/',
         OrderCompletedCountView.as_view(), name='completed-order-count'),
    path('offerdetails/<int:id>/', OfferDetailView.as_view(), name='offerdetail'),
    path('', include(router.urls)),
]
