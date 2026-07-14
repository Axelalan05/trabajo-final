import django_filters
from apps.juegos.models import Juego

class JuegoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    genero = django_filters.CharFilter(lookup_expr='icontains')
    plataforma = django_filters.CharFilter(lookup_expr='icontains')
    estado = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Juego
        fields = ['nombre', 'genero', 'plataforma', 'estado']