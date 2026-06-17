from rest_framework import serializers
from apps.juegos.models import Juego

class JuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Juego
        fields = ('id', 'nombre', 'genero', 'plataforma', 'imagen', 'descripcion', 'anio', 'estado', 'puntaje', 'resenia', 'created_at')
        read_only_fields = ('id', 'created_at')