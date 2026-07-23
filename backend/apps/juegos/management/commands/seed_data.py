import random
import time

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.juegos import rawg_service
from apps.juegos.models import Juego, UserJuego
from apps.juegos.serializers import JuegoSerializer

JUEGOS_SEED = [
    'Elden Ring',
    'The Legend of Zelda: Breath of the Wild',
    'God of War',
    'Red Dead Redemption 2',
    'The Witcher 3: Wild Hunt',
    'Portal 2',
    'Hollow Knight',
    'Hades',
    'Disco Elysium',
    'Resident Evil 4',
    'Stardew Valley',
    'Celeste',
    'Dark Souls III',
    'Minecraft',
    'Grand Theft Auto V',
]

TOTAL_USUARIOS = 50
USUARIOS_POR_JUEGO_GRUPO_A = 4  # primeros 5 juegos
USUARIOS_POR_JUEGO_GRUPO_B = 3  # siguientes 10 juegos
PASSWORD_SEED = 'seed12345'


class Command(BaseCommand):
    help = 'Carga un catálogo de 15 juegos (vía RAWG) y 50 usuarios de prueba, uniéndolos a juegos.'

    def handle(self, *args, **options):
        juegos_creados = self._crear_juegos()
        usuarios = self._crear_usuarios()
        self._unir_usuarios_a_juegos(juegos_creados, usuarios)

    def _crear_juegos(self):
        juegos = []
        for titulo in JUEGOS_SEED:
            try:
                resultados = rawg_service.buscar_juegos(titulo, page_size=1)
            except rawg_service.RawgError as exc:
                self.stdout.write(self.style.ERROR(f'Error buscando "{titulo}": {exc}'))
                continue

            if not resultados:
                self.stdout.write(self.style.WARNING(f'Sin resultados en RAWG para "{titulo}", se salta.'))
                continue

            rawg_id = resultados[0]['rawg_id']

            existente = Juego.objects.filter(rawg_id=rawg_id).first()
            if existente:
                self.stdout.write(f'"{titulo}" ya está en el catálogo, se reutiliza.')
                juegos.append(existente)
                continue

            try:
                detalle = rawg_service.obtener_detalle(rawg_id)
            except rawg_service.RawgError as exc:
                self.stdout.write(self.style.ERROR(f'Error trayendo detalle de "{titulo}": {exc}'))
                continue

            serializer = JuegoSerializer(data=detalle)
            if serializer.is_valid():
                juego = serializer.save()
                juegos.append(juego)
                self.stdout.write(self.style.SUCCESS(f'Creado: {juego.nombre}'))
            else:
                self.stdout.write(self.style.ERROR(f'"{titulo}" no pasó la validación: {serializer.errors}'))

            time.sleep(0.3)  # para no saturar la API de RAWG

        return juegos

    def _crear_usuarios(self):
        usuarios = []
        for i in range(1, TOTAL_USUARIOS + 1):
            username = f'jugador{i}'
            user, creado = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@gamevault.test'},
            )
            if creado:
                user.set_password(PASSWORD_SEED)
                user.save()
                self.stdout.write(f'Usuario creado: {username}')
            usuarios.append(user)
        return usuarios

    def _unir_usuarios_a_juegos(self, juegos, usuarios):
        if not juegos:
            self.stdout.write(self.style.WARNING('No hay juegos para asignar usuarios.'))
            return

        estados = [e[0] for e in UserJuego.ESTADOS]
        pool_usuarios = iter(usuarios)
        uniones_creadas = 0

        grupo_a = juegos[:5]
        grupo_b = juegos[5:15]

        for juego in grupo_a:
            uniones_creadas += self._unir_grupo(juego, pool_usuarios, USUARIOS_POR_JUEGO_GRUPO_A, estados)

        for juego in grupo_b:
            uniones_creadas += self._unir_grupo(juego, pool_usuarios, USUARIOS_POR_JUEGO_GRUPO_B, estados)

        self.stdout.write(self.style.SUCCESS(f'\nUniones usuario-juego creadas: {uniones_creadas}'))

    def _unir_grupo(self, juego, pool_usuarios, cantidad, estados):
        creadas = 0
        for _ in range(cantidad):
            user = next(pool_usuarios, None)
            if user is None:
                self.stdout.write(self.style.WARNING('Se acabaron los usuarios antes de terminar de asignar.'))
                break

            _, creado = UserJuego.objects.get_or_create(
                user=user,
                juego=juego,
                defaults={
                    'estado': random.choice(estados),
                    'puntaje': random.randint(1, 10) if random.random() > 0.3 else None,
                },
            )
            if creado:
                creadas += 1
        return creadas