from django.contrib.auth.models import User
from django.db import models

# Usamos el User built-in de Django (django.contrib.auth.models.User).
# Sus campos son: id, username, email, password, first_name, last_name,
#                 is_active, is_staff, date_joined, last_login.
#
# Si en el futuro necesitás campos extra (avatar, bio, etc.), el patrón
# recomendado es agregar un modelo Profile con OneToOneField(User, ...).

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    def __str__(self):
        return f'Perfil de {self.user.username}'
    
class PendingRegistration(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=128)  # contraseña hasheada
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Registro pendiente de {self.username} ({self.email})'
