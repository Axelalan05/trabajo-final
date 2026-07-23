from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password as dj_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from apps.users.models import Profile, PendingRegistration

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate_email(self, value):
        # No verificamos duplicado aquí porque el usuario aún no se crea
        return value

    def validate_password(self, value):
        try:
            dj_validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm': 'Las contraseñas no coinciden.'}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined', 'is_staff')
        read_only_fields = ('id', 'date_joined', 'is_staff')
        

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Profile
        fields = ('username', 'email', 'bio', 'avatar')
    
    def validate_bio(self, value):
        if len(value) > 500:
            raise serializers.ValidationError('La bio no puede superar los 500 caracteres.')
        return value
        
class ProfilePublicoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'avatar')
        
class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            # No revelamos si el email existe o no
            pass
        return value

class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.IntegerField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {"password_confirm": "Las contraseñas no coinciden."}
            )

        try:
            user = User.objects.get(pk=data['uid'])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"uid": "El enlace es inválido o ha expirado."}
            )

        from .password_reset import check_reset_token
        if not check_reset_token(user, data['token']):
            raise serializers.ValidationError(
                {"token": "El enlace es inválido o ha expirado."}
            )

        data['user'] = user
        return data

class VerifyEmailSerializer(serializers.Serializer):
    uid = serializers.IntegerField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            pending = PendingRegistration.objects.get(pk=data['uid'])
        except PendingRegistration.DoesNotExist:
            raise serializers.ValidationError(
                {"uid": "El enlace es inválido o ha expirado."}
            )

        if pending.token != data['token']:
            raise serializers.ValidationError(
                {"token": "El enlace es inválido o ha expirado."}
            )

        from django.utils import timezone
        from datetime import timedelta
        if timezone.now() - pending.created_at > timedelta(hours=24):
            pending.delete()
            raise serializers.ValidationError(
                {"uid": "El enlace ha expirado. Registrate nuevamente."}
            )

        data['pending'] = pending
        return data

class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined', 'is_staff', 'is_active')

class AdminUserDetailSerializer(serializers.ModelSerializer):
    """Para mostrar datos del usuario + sus juegos"""
    juegos = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined', 'is_staff', 'is_active', 'juegos')

    def get_juegos(self, obj):
        from apps.juegos.models import UserJuego
        user_juegos = UserJuego.objects.filter(user=obj).select_related('juego')
        return [
            {
                'juego_id': uj.juego.id,
                'juego_nombre': uj.juego.nombre,
                'juego_imagen': uj.juego.imagen_url,
                'estado': uj.estado,
                'puntaje': uj.puntaje,
                'resenia': uj.resenia,
            }
            for uj in user_juegos
        ]
