from rest_framework import serializers
from apps.juegos.models import Juego, UserJuego
from datetime import date


class JuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Juego
        fields = ('id', 'nombre', 'genero', 'plataforma', 'imagen', 'descripcion', 'anio', 'created_at')
        read_only_fields = ('id', 'created_at')

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError('El nombre no puede estar vacío.')
        return value.strip()

    def validate_anio(self, value):
        anio_actual = date.today().year
        if value > anio_actual + 1:
            raise serializers.ValidationError(f'El año no puede ser mayor a {anio_actual + 1}.')
        if value < 1970:
            raise serializers.ValidationError('El año no puede ser anterior a 1970.')
        return value

    def validate(self, attrs):
        nombre = attrs.get('nombre', '')
        qs = Juego.objects.filter(nombre__iexact=nombre)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Ya existe un juego con ese nombre en el catálogo.')
        return attrs


class UserJuegoSerializer(serializers.ModelSerializer):
    juego = JuegoSerializer(read_only=True)
    juego_id = serializers.PrimaryKeyRelatedField(
        queryset=Juego.objects.all(), source='juego', write_only=True
    )

    class Meta:
        model = UserJuego
        fields = ('id', 'juego', 'juego_id', 'estado', 'puntaje', 'resenia', 'created_at')
        read_only_fields = ('id', 'created_at')

    def validate(self, attrs):
        request = self.context.get('request')
        juego = attrs.get('juego')
        if request and not self.instance and UserJuego.objects.filter(user=request.user, juego=juego).exists():
            raise serializers.ValidationError('Ya estás en este juego.')
        return attrs
    
    def validate_puntaje(self, value):
        if value is not None and (value < 1 or value > 10):
            raise serializers.ValidationError('El puntaje debe estar entre 1 y 10.')
        return value