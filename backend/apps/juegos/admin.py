from django.contrib import admin
from apps.juegos.models import Juego, UserJuego


@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'genero', 'plataforma', 'fecha_lanzamiento', 'created_at')
    list_filter = ('genero', 'plataforma')
    search_fields = ('nombre', 'rawg_id')
    ordering = ('-created_at',)


@admin.register(UserJuego)
class UserJuegoAdmin(admin.ModelAdmin):
    list_display = ('user', 'juego', 'estado', 'puntaje', 'created_at')
    list_filter = ('estado',)
    search_fields = ('user__username', 'juego__nombre')
    autocomplete_fields = ('user', 'juego')
    ordering = ('-created_at',)