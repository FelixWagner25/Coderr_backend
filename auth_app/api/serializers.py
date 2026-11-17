from rest_framework import serializers
from coderr_app.models import User


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        error_msg = 'Login data is invalid.'

        if not User.objects.filter(email__iexact=data['email']).exists():
            raise serializers.ValidationError({error_msg})

        user = User.objects.get(email__iexact=data['email'])
        if not user.check_password(data['password']):
            raise serializers.ValidationError({error_msg})

        data['user'] = user
        return data
