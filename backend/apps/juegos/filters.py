import re
import django_filters
from django.db.models import Q
from apps.juegos.models import Juego


def _expandir_busqueda_plataforma(valor: str) -> Q:
    match = re.fullmatch(r'(?i)ps\s*(\d)?', valor.strip())
    if match:
        numero = match.group(1)
        if numero:
            return Q(plataforma__icontains=f'PlayStation {numero}')
        return Q(plataforma__icontains='PlayStation')
    return Q(plataforma__icontains=valor)


class JuegoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    genero = django_filters.CharFilter(lookup_expr='icontains')
    plataforma = django_filters.CharFilter(method='filter_plataforma')

    class Meta:
        model = Juego
        fields = ['nombre', 'genero', 'plataforma']

    def filter_plataforma(self, queryset, name, value):
        return queryset.filter(_expandir_busqueda_plataforma(value))