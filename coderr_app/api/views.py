from django.db.models import Q
from django.shortcuts import get_object_or_404
from coderr_app.models import OfferDetail, Order, User
from rest_framework import filters, generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from ..models import BusinessUserProfile, CustomerProfile, Review
from .serializers import BusinessProfileSerializer, CustomerProfileSerializer, OfferCreateSerializer, OfferDetailSerializer, OfferListSerializer, OfferRetrieveSerializer, OfferUpdateSerializer, OrderCreateSerializer, OrderUpdateSerializer, OrderListSerializer, ProfileDetailSerializer, ReviewListCreateSerializer, ReviewUpdateSerializer
from .permissions import IsObjectCreator, IsOrderBusinessUser, IsReviewer, IsUserTypeCustomer, IsUserTypeBusinessUser


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
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class OrderDetailView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    lookup_url_kwarg = 'id'
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsAuthenticated,
                          IsUserTypeBusinessUser, IsOrderBusinessUser]


class OrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        user = get_object_or_404(User, id=business_user_id)

        order_count = Order.objects.filter(Q(status=Order.OrderStatus.IN_PROGRESS) & Q(
            business_user=user)).count()
        return Response({'order_count': order_count})


class OrderCompletedCountView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        user = get_object_or_404(User, id=business_user_id)

        completed_order_count = Order.objects.filter(Q(status=Order.OrderStatus.COMPLETED) & Q(
            business_user=user)).count()
        return Response({'completed_order_count': completed_order_count})


class ReviewViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    lookup_url_kwarg = 'id'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated_at', 'rating']
    ordering = ['updated_at']

    def get_queryset(self):
        queryset = Review.objects.all()

        business_user_param = self.request.query_params.get(
            'business_user_id', None)
        if business_user_param is not None:
            queryset = queryset.filter(business_user=business_user_param)

        reviewer_param = self.request.query_params.get('reviewer_id', None)
        if reviewer_param is not None:
            queryset = queryset.filter(reviewer=reviewer_param)

        return queryset

    def get_serializer_class(self):
        if self.action in ['list', 'create']:
            return ReviewListCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ReviewUpdateSerializer
        else:
            return None

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsUserTypeCustomer]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsReviewer]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class OfferViewSet(viewsets.ModelViewSet):
    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        if self.action == 'list':
            return OfferListSerializer
        elif self.action == 'retrieve':
            return OfferRetrieveSerializer
        elif self.action == 'create':
            return OfferCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OfferUpdateSerializer
        else:
            return None

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsUserTypeBusinessUser]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsObjectCreator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OfferDetailView(generics.RetrieveAPIView):
    lookup_url_kwarg = 'id'
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]


class BusinessProfileView(generics.ListAPIView):
    queryset = BusinessUserProfile.objects.all()
    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]


class CustomerProfileView(generics.ListAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]


class ProfileDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = ProfileDetailSerializer

    def get_permissions(self):
        if self.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.method == 'PATCH':
            permission_classes = [IsAuthenticated, IsObjectCreator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
