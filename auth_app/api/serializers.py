from rest_framework import serializers
from coderr_app.models import User


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        error_msg = 'Login data is invalid.'

        if not User.objects.filter(username__iexact=data['username']).exists():
            raise serializers.ValidationError({error_msg})

        user = User.objects.get(username__iexact=data['username'])
        if not user.check_password(data['password']):
            raise serializers.ValidationError({error_msg})

        data['user'] = user
        return data
