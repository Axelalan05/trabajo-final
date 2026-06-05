from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.users.serializers import RegisterSerializer, UserSerializer
from core.response import ApiResponse


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return ApiResponse.success(
                data=UserSerializer(user).data,
                status=201
            )
        return ApiResponse.error(
            code="validation_error",
            message="Invalidad data",
            details=serializer.erros,
            status=400
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return ApiResponse.success(status=204)
        except Exception:
            return ApiResponse.error(
                code='invalid_token',
                message='Invalid or expired token',
                status=400
            )
