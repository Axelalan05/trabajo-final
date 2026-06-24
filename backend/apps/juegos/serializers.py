from rest_framework import serializers
from apps.juegos.models import Juego
from datetime import date

class JuegoSerializer(serializers.ModelSerializer):
    es_favorito = serializers.SerializerMethodField()
    
    class Meta:
        model = Juego
        fields = ('id', 'nombre', 'genero', 'plataforma', 'imagen', 'descripcion', 'anio', 'estado', 'puntaje', 'resenia', 'created_at', 'es_favorito')
        read_only_fields = ('id', 'created_at')
        
    def get_es_favorito(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favoritos.filter(id=request.user.id).exists()
        return False

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

    def validate_puntaje(self, value):
        if value is not None and (value < 1 or value > 10):
            raise serializers.ValidationError('El puntaje debe estar entre 1 y 10.')
        return value