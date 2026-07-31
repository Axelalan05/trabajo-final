from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from apps.users.serializers import (
    RegisterSerializer, UserSerializer, ProfileSerializer,
    ProfilePublicoSerializer, RequestPasswordResetSerializer,
    ResetPasswordSerializer, VerifyEmailSerializer,
    AdminUserListSerializer, AdminUserDetailSerializer
)
from apps.users.models import Profile, PendingRegistration
from core.response import ApiResponse


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.error(
                code="validation_error",
                message="Invalidad data",
                details=serializer.errors,
                status=400
            )

        validated_data = serializer.validated_data

        if User.objects.filter(email=validated_data['email']).exists():
            return ApiResponse.error(
                code="validation_error",
                message="El email ya está en uso.",
                details={"email": ["El email ya está en uso."]},
                status=400
            )

        existing_pending = PendingRegistration.objects.filter(
            email=validated_data['email']
        ).first()
        if existing_pending:
            existing_pending.delete()

        import secrets
        token = secrets.token_urlsafe(32)

        from django.contrib.auth.hashers import make_password
        hashed_password = make_password(validated_data['password'])

        pending = PendingRegistration.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=hashed_password,
            token=token,
        )

        email_sent = send_verification_email(
            username=pending.username,
            email=pending.email,
            uid=pending.pk,
            token=token,
        )

        return ApiResponse.success(
            data={
                "message": "Registro iniciado. Revisá tu correo para confirmar tu cuenta.",
                "email_sent": email_sent,
                "verification_url": f"{settings.FRONTEND_URL}/verify-email/{pending.pk}/{token}",  # ← agregá esto
            },
            status=201
        )


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


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
            
class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return ApiResponse.success(data=serializer.data)

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

from .password_reset import send_reset_email, send_verification_email
from .serializers import RequestPasswordResetSerializer, ResetPasswordSerializer


class RequestPasswordResetView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RequestPasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.error(
                code="validation_error",
                message="Correo inválido",
                details=serializer.errors,
                status=400
            )

        email = serializer.validated_data['email']

        reset_url = None

        try:
            user = User.objects.get(email=email, is_active=True)
            success, token = send_reset_email(user, request)
            if token:
                reset_url = f"{settings.FRONTEND_URL}/reset-password/{user.pk}/{token}"
        except User.DoesNotExist:
            pass

        return ApiResponse.success(
            data={
                "message": "Si el correo está registrado, recibirás un enlace para restablecer tu contraseña.",
                "reset_url": reset_url,
            }
        )


class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.error(
                code="validation_error",
                message="Datos inválidos",
                details=serializer.errors,
                status=400
            )

        user = serializer.validated_data['user']
        password = serializer.validated_data['password']

        user.set_password(password)
        user.save()

        return ApiResponse.success(
            data={"message": "Contraseña actualizada correctamente."}
        )

class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.error(
                code="validation_error",
                message="Error de verificación",
                details=serializer.errors,
                status=400
            )

        pending = serializer.validated_data['pending']

        user = User.objects.create_user(
            username=pending.username,
            email=pending.email,
        )
        user.password = pending.password
        user.save()

        pending.delete()

        return ApiResponse.success(
            data={
                "message": "Cuenta confirmada exitosamente. Ya podés iniciar sesión."
            },
            status=201
        )

from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter


class AdminUserPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100


class AdminUserListView(generics.ListAPIView):
    serializer_class = AdminUserListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = AdminUserPagination
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email', 'juegos_usuario__juego__nombre']

    def get_queryset(self):
        if not self.request.user.is_staff:
            return User.objects.none()
        return User.objects.all().order_by('username').distinct()

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return ApiResponse.error(
                code="permission_denied",
                message="No tenés permisos de administrador.",
                status=403
            )
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data={'users': serializer.data})

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'data': {
                'users': data,
                'total': self.paginator.page.paginator.count,
                'page': self.paginator.page.number,
                'total_pages': self.paginator.page.paginator.num_pages,
            }
        })


class AdminUserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return ApiResponse.error(
                code="permission_denied",
                message="No tenés permisos de administrador.",
                status=403
            )
        user = self.get_object()
        if user == request.user:
            return ApiResponse.error(
                code="self_delete",
                message="No podés eliminar tu propio usuario.",
                status=400
            )
        username = user.username
        user.delete()
        return ApiResponse.success(
            data={"message": f"Usuario '{username}' eliminado correctamente."}
        )


class AdminUserDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return ApiResponse.error(
                code="permission_denied",
                message="No tenés permisos de administrador.",
                status=403
            )
        user = self.get_object()
        serializer = AdminUserDetailSerializer(user)
        return ApiResponse.success(data=serializer.data)