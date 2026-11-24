from rest_framework import serializers
from coderr_app.models import Offer, OfferDetail, Order, Review, User


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


class OfferRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer


class OfferUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer


class OfferDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ['title', 'revisions',
                            'delivery_time_in_days', 'price', 'features', 'offer_type']
