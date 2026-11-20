from django.db.models import Q
from django.shortcuts import get_object_or_404
from coderr_app.models import OfferDetail, Order
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderCreateSerializer, OrderUpdateSerializer, OrderListSerializer
from .permissions import IsOrderBusinessUser, IsUserTypeCustomer, IsUserTypeBusinessUser


class OrderListCreateView(generics.ListCreateAPIView):

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer=user) | Q(business_user=user)).distinct()

    def perform_create(self, serializer):
        offer_detail_id = serializer.validated_data['offer_detail_id']
        offer_detail = get_object_or_404(OfferDetail, id=offer_detail_id)
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
            permission_classes = [IsAuthenticated, IsUserTypeCustomer]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class OrderDetailView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    lookup_url_kwarg = 'id'
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsAuthenticated,
                          IsUserTypeBusinessUser, IsOrderBusinessUser]


class OrderCountView(generics.ListAPIView):
    pass


class OrderCompletedCountView(generics.ListAPIView):
    pass
