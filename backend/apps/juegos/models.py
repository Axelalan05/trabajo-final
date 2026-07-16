from django.contrib.auth.models import User
from django.db import models


class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    plataforma = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='juegos/', blank=True, null=True)
    descripcion = models.TextField(blank=True)
    anio = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre} ({self.plataforma})'


class UserJuego(models.Model):
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