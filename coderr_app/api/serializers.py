from django.db.models import Min
from django.http import HttpResponseBadRequest
from rest_framework import serializers
from coderr_app.models import BusinessUserProfile, CustomerProfile, Offer, OfferDetail, Order, Review, User


class OrderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'customer', 'business_user', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'business_user', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at', 'offer_detail_id']
        read_only_fields = ['id', 'customer', 'business_user', 'title', 'revisions', 'delivery_time_in_days',
                            'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data.pop('offer_detail_id')
        return Order.objects.create(**validated_data)


class OrderUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'customer', 'business_user', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'customer', 'business_user', 'title', 'revisions', 'delivery_time_in_days',
                            'price', 'features', 'offer_type', 'created_at', 'updated_at']


class ReviewListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating',
                  'description', 'created_at', 'updated_at']
        read_only_fields = ['reviewer', 'created_at', 'updated_at']

    def validate(self, data):
        reviewer = self.context['request'].user
        business_user = data['business_user']

        if business_user.type != User.UserType.BUSINESS:
            raise serializers.ValidationError(
                {'business_user': 'User is no business user.'})

        if Review.objects.filter(reviewer=reviewer, business_user=business_user).exists():
            raise serializers.ValidationError(
                'You already reviewed this business.')

        return data


class ReviewUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating',
                  'description', 'created_at', 'updated_at']
        read_only_fields = ['business_user',
                            'reviewer', 'created_at', 'updated_at']


class OfferListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer


class OfferCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='offerdetail', lookup_url_kwarg='id')

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']


class OfferRetrieveSerializer(serializers.ModelSerializer):
    details = OfferDetailLinkSerializer(
        source='offerdetails', many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at',
                  'updated_at', 'details', 'min_price', 'min_delivery_time']

    def get_min_price(self, obj):
        return obj.offerdetails.aggregate(min=Min('price'))['min']

    def get_min_delivery_time(self, obj):
        return obj.offerdetails.aggregate(min=Min('delivery_time_in_days'))['min']


class OfferDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type']

    def validate(self, data):
        required_fields = ['title', 'revisions',
                           'delivery_time_in_days', 'price', 'features', 'offer_type']
        errors = {}
        for field in required_fields:
            if field not in data:
                errors[field] = 'This field is required'

        if errors:
            raise serializers.ValidationError(errors)

        return data


class OfferUpdateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(
        many=True, source='offerdetails', required=False)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def update(self, instance, validated_data):
        details = validated_data.pop('offerdetails', [])
        instance = super().update(instance, validated_data)

        for detail in details:
            OfferDetail.objects.update_or_create(
                offer=instance, offer_type=detail['offer_type'], defaults=detail)

        return instance


class BusinessProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)

    class Meta:
        model = BusinessUserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file',
                  'location', 'tel', 'description', 'working_hours', 'type']


class CustomerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)
    uploaded_at = serializers.FileField(source='file', read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['user', 'username', 'first_name',
                  'last_name', 'file', 'uploaded_at', 'type']


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id')
    file = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    tel = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    working_hours = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(source='date_joined')

    class Meta:
        model = User
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location',
                  'tel', 'description', 'working_hours', 'type', 'email', 'created_at']
        read_only_fields = ['user', 'username', 'file', 'type', 'created_at']

    def get_location(self, obj):
        if obj.type == User.UserType.BUSINESS:
            return obj.business_profile.location
        else:
            return ''

    def get_tel(self, obj):
        if obj.type == User.UserType.BUSINESS:
            return obj.business_profile.tel
        else:
            ''

    def get_description(self, obj):
        if obj.type == User.UserType.BUSINESS:
            return obj.business_profile.description
        else:
            ''

    def get_working_hours(self, obj):
        if obj.type == User.UserType.BUSINESS:
            return obj.business_profile.working_hours
        else:
            ''

    def get_file(self, obj):
        if obj.type == User.UserType.BUSINESS:
            file_obj = obj.business_profile.file
        elif obj.type == User.UserType.CUSTOMER:
            file_obj = obj.customer_profile.file
        else:
            return None

        if file_obj and file_obj.file:
            return file_obj.file.url

        return None
