from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Juego(models.Model):
    ESTADOS = [
        ('jugando', 'Jugando'),
        ('completado', 'Completado'),
        ('pendiente', 'Pendiente'),
        ('abandonado', 'Abandonado'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='juegos')
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    plataforma = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='juegos/', blank=True, null=True)
    descripcion = models.TextField(blank=True)
    anio = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    puntaje = models.IntegerField(null=True, blank=True)
    resenia = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    favoritos = models.ManyToManyField(User, related_name='juegos_favoritos', blank=True)
    
    
    def __str__(self):
        return f'{self.nombre} ({self.plataforma})'