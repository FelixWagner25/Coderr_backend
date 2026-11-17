from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import UserLoginSerializer


class LoginView(APIView):
    "Authenticates a user and returns the user token."

    permission_classes = [AllowAny]

    def post(self, request):
        """Validates user credentials and returns the user data as JSON."""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user_token = Token.objects.get(user=user).key
            return Response({"token": user_token, "fullname": user.get_full_name(), "email": user.email, "user_id": user.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
