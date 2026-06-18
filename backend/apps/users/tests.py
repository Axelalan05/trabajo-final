from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import Profile


class RegistroTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_registro_exitoso(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'nuevouser',
            'email': 'nuevo@test.com',
            'password': 'Test1234!',
            'password_confirm': 'Test1234!'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_email_ya_registrado(self):
        User.objects.create_user(
            username='existente',
            email='existente@test.com',
            password='Test1234!'
        )
        response = self.client.post('/api/auth/register/', {
            'username': 'otrouser',
            'email': 'existente@test.com',
            'password': 'Test1234!',
            'password_confirm': 'Test1234!'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_passwords_no_coinciden(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'otrouser',
            'email': 'otro@test.com',
            'password': 'Test1234!',
            'password_confirm': 'OtraPassword!'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_debil(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'otrouser',
            'email': 'otro@test.com',
            'password': '123',
            'password_confirm': '123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
class ProfileTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='Test1234!',
            email='test@test.com'
        )
        Profile.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_ver_perfil_propio(self):
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['username'], 'testuser')

    def test_editar_perfil(self):
        response = self.client.patch('/api/auth/profile/', {
            'bio': 'Mi nueva bio'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_perfil_publico_sin_email(self):
        response = self.client.get('/api/auth/users/testuser/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('email', response.data['data'])

    def test_perfil_publico_usuario_inexistente(self):
        response = self.client.get('/api/auth/users/noexiste/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)