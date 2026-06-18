from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.users.serializers import RegisterSerializer, UserSerializer, ProfileSerializer, ProfilePublicoSerializer
from apps.users.models import Profile
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
            details=serializer.errors,
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

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return ApiResponse.success(data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(data=serializer.data)
        return ApiResponse.error(
            code='validation_error',
            message='Invalid data',
            details=serializer.errors,
            status=400
        )

class ProfilePublicoView(generics.RetrieveAPIView):
    serializer_class = ProfilePublicoSerializer
    permission_classes = [AllowAny]
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'
    queryset = Profile.objects.all()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return ApiResponse.success(data=serializer.data)
