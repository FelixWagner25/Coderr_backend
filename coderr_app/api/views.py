from coderr_app.models import Order
from rest_framework import generics


class OrderListCreateView(generics.ListCreateAPIView):
    pass


class OrderDetailView(generics.UpdateAPIView):
    pass


class OrderCountView(generics.ListAPIView):
    pass


class OrderCompletedCountView(generics.ListAPIView):
    pass
