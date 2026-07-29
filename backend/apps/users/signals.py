from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import Profile


@receiver(post_save, sender=User)
def crear_perfil_automaticamente(sender, instance, created, **kwargs):
    """
    Cada vez que se crea un User (registro normal, verificación de
    email, createsuperuser, Django admin, seed_data, etc.) le creamos
    su Profile en el mismo momento. Así evitamos que el perfil público
    de un usuario tire 404 solo porque todavía no visitó "Mi perfil".
    """
    if created:
        Profile.objects.get_or_create(user=instance)