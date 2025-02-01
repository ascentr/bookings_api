from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from .serializers import UserSerializer, LoginSerializer


class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                'status': 'success',
                'message': 'Account created successfully',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            return Response({
                'status': 'success',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
                'user': UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"error": "No Refresh Token"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"status": "success", "message": "Logout Successful"},
                            status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


"""
{
    "name": "John Doe",
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword",
    "phone_number": "1234567890"
}

{
    "email": "john@example.com",
    "password": "securepassword"
}

"""

