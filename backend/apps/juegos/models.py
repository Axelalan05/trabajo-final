from django.contrib.auth.models import User
from django.db import models


class Juego(models.Model):
    """
    Catálogo de juegos. Los datos vienen de la API de RAWG — el admin
    busca y selecciona un juego, y estos campos se llenan a partir de
    ahí (no se tipean a mano, salvo que RAWG no tenga el dato).
    """
    rawg_id = models.IntegerField(unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=200)
    genero = models.CharField(max_length=255)       # ej: "Action, RPG"
    plataforma = models.CharField(max_length=255)    # ej: "PC, PlayStation 5"
    imagen_url = models.URLField(blank=True, null=True)
    descripcion = models.TextField(blank=True)
    fecha_lanzamiento = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre} ({self.plataforma})'


class UserJuego(models.Model):
    """
    Relación entre un usuario y un juego del catálogo.
    Acá vive todo lo que es personal de cada usuario: su estado
    de avance, su puntaje, su reseña.
    """
    ESTADOS = [
        ('jugando', 'Jugando'),
        ('completado', 'Completado'),
        ('pendiente', 'Pendiente'),
        ('abandonado', 'Abandonado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='juegos_usuario')
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='usuarios_juego')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    puntaje = models.IntegerField(null=True, blank=True)
    resenia = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'juego')

    def __str__(self):
        return f'{self.user.username} - {self.juego.nombre} ({self.estado})'