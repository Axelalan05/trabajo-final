from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.juegos.models import Juego


class JuegoValidacionTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='Test1234!',
            email='test@test.com'
        )
        self.client.force_authenticate(user=self.user)

    def test_puntaje_fuera_de_rango(self):
        response = self.client.post('/api/juegos/', {
            'nombre': 'God of War',
            'genero': 'Acción',
            'plataforma': 'PS4',
            'descripcion': 'Excelente',
            'anio': 2018,
            'estado': 'completado',
            'puntaje': 15
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_anio_futuro(self):
        response = self.client.post('/api/juegos/', {
            'nombre': 'Juego Futuro',
            'genero': 'Acción',
            'plataforma': 'PS5',
            'descripcion': 'No existe',
            'anio': 2099,
            'estado': 'pendiente',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_juego_exitoso(self):
        response = self.client.post('/api/juegos/', {
            'nombre': 'The Last of Us',
            'genero': 'Aventura',
            'plataforma': 'PS4',
            'descripcion': 'Increíble',
            'anio': 2013,
            'estado': 'completado',
            'puntaje': 10
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class FavoritosTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='Test1234!',
            email='test@test.com'
        )
        self.client.force_authenticate(user=self.user)
        self.juego = Juego.objects.create(
            user=self.user,
            nombre='Hollow Knight',
            genero='Metroidvania',
            plataforma='PC',
            anio=2017,
            estado='completado',
            puntaje=9
        )

    def test_agregar_favorito(self):
        response = self.client.post(f'/api/juegos/{self.juego.id}/favorito/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user, self.juego.favoritos.all())

    def test_quitar_favorito(self):
        self.juego.favoritos.add(self.user)
        response = self.client.post(f'/api/juegos/{self.juego.id}/favorito/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.user, self.juego.favoritos.all())


class EstadisticasTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='Test1234!',
            email='test@test.com'
        )
        self.client.force_authenticate(user=self.user)
        Juego.objects.create(
            user=self.user,
            nombre='Hollow Knight',
            genero='Metroidvania',
            plataforma='PC',
            anio=2017,
            estado='completado',
            puntaje=9
        )

    def test_estadisticas(self):
        response = self.client.get('/api/juegos/estadisticas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['juegos_completados'], 1)
        self.assertEqual(response.data['data']['promedio_puntaje'], 9.0)
