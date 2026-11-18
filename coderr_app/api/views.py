from django.db.models import Q
from coderr_app.models import Order
from rest_framework import generics
from .serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer=user) | Q(business_user=user)).distinct()

    def perform_create(self, serializer):
        pass


class OrderDetailView(generics.UpdateAPIView):
    pass


class OrderCountView(generics.ListAPIView):
    pass


class OrderCompletedCountView(generics.ListAPIView):
    pass
