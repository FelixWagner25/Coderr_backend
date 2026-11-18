from coderr_app.models import Order
from rest_framework import generics
from .serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        pass


class OrderDetailView(generics.UpdateAPIView):
    pass


class OrderCountView(generics.ListAPIView):
    pass


class OrderCompletedCountView(generics.ListAPIView):
    pass
