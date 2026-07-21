from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password as dj_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from apps.users.models import Profile


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
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('El email ya está en uso.')
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
