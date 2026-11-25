from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessProfileView, CustomerProfileView, OfferDetailView, OfferViewSet, OrderCompletedCountView, OrderCountView, OrderDetailView, OrderListCreateView, ProfileDetailView, ReviewViewSet

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'offers', OfferViewSet, basename='offer')

urlpatterns = [
    path('completed-order-count/<int:business_user_id>/',
         OrderCompletedCountView.as_view(), name='completed-order-count'),
    path('offerdetails/<int:id>/', OfferDetailView.as_view(), name='offerdetail'),
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:business_user_id>/',
         OrderCountView.as_view(), name='order-count'),
    path('profiles/business/', BusinessProfileView.as_view(),
         name='business-profile-list'),
    path('profiles/customer/', CustomerProfileView.as_view(),
         name='customer-profile-list'),
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
    path('', include(router.urls)),
]
