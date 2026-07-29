"""
Comando de uso único: crea el Profile faltante para todo User que
todavía no tenga uno (por ejemplo, usuarios seed o cualquiera que
nunca visitó "Mi perfil" antes de que existiera el signal).

Uso:
    python manage.py backfill_profiles

Ubicación: backend/apps/users/management/commands/backfill_profiles.py
(hace falta crear también los __init__.py vacíos en
apps/users/management/ y apps/users/management/commands/ si no existen)
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.users.models import Profile


class Command(BaseCommand):
    help = 'Crea el Profile faltante para los usuarios que no lo tienen todavía.'

    def handle(self, *args, **options):
        creados = 0
        for user in User.objects.all():
            _, created = Profile.objects.get_or_create(user=user)
            if created:
                creados += 1
        total = User.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'Listo. Perfiles creados: {creados} / {total} usuarios totales.'
        ))