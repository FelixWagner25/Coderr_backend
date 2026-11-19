from django.db.models import Q
from coderr_app.models import OfferDetail, Order
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderCreateSerializer, OrderListSerializer
from .permissions import UserIsCustomer


class OrderListCreateView(generics.ListCreateAPIView):

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer=user) | Q(business_user=user)).distinct()

    def perform_create(self, serializer):
        offer_detail_id = serializer.validated_data['offer_detail_id']
        offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        serializer.save(customer=self.request.user, business_user=offer_detail.offer.user, title=offer_detail.title, revisions=offer_detail.revisions,
                        delivery_time_in_days=offer_detail.delivery_time_in_days, price=offer_detail.price, features=offer_detail.features, offer_type=offer_detail.offer_type)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderListSerializer
        elif self.request.method == 'POST':
            return OrderCreateSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'POST':
            permission_classes = [IsAuthenticated, UserIsCustomer]
        return [permission() for permission in permission_classes]


class OrderDetailView(generics.UpdateAPIView):
    pass


class OrderCountView(generics.ListAPIView):
    pass


class OrderCompletedCountView(generics.ListAPIView):
    pass
