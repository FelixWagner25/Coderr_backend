from django.db.models import Q
from coderr_app.models import Order
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer
from .permissions import UserIsCustomer


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer=user) | Q(business_user=user)).distinct()

    def perform_create(self, serializer):
        pass

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
