from rest_framework import serializers
from coderr_app.models import Order, Review


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


class ReviewSerializer(serializers.ModelField):

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating',
                  'description', 'created_at', 'updated_at']
        read_only_fields = ['reviewer', 'created_at', 'updated_at']

    # Validation whether customer has already a review for business_user is required
