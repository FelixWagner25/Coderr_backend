from rest_framework import serializers
from coderr_app.models import User
from rest_framework.authtoken.models import Token


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Validates and converts registration request data to python applicable data. Creates new user with validated data and an authentication token."""

    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'password', 'repeated_password', 'type']

    def validate(self, data):
        """Validates congruency of entered passwords and if username or email are free."""
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError(
                {'password': 'Entered passwords do not match.'})
        if User.objects.filter(username__iexact=data['username']).exists():
            raise serializers.ValidationError(
                {'username': 'Username is already used.'})
        if User.objects.filter(email__iexact=data['email']).exists():
            raise serializers.ValidationError(
                {'email': 'Email is already used.'})
        return data

    def create(self, validated_data):
        """Creates new user and its authentication token."""
        validated_data.pop('repeated_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            type=validated_data['type']
        )
        Token.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Validates and converts login request data to python applicable data."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Validates user login request data."""
        error_msg = 'Login data is invalid.'

        if not User.objects.filter(username__iexact=data['username']).exists():
            raise serializers.ValidationError({error_msg})

        user = User.objects.get(username__iexact=data['username'])
        if not user.check_password(data['password']):
            raise serializers.ValidationError({error_msg})

        data['user'] = user
        return data
