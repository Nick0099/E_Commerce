from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email    = 'test@test.com',
            name     = 'Test User',
            password = 'TestPass123!'
        )

    def test_user_created_with_email(self):
        self.assertEqual(self.user.email, 'test@test.com')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'test@test.com')

    def test_user_is_not_seller_by_default(self):
        self.assertFalse(self.user.is_seller)

    def test_user_login_field_is_email(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')


class AuthAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email    = 'auth@test.com',
            name     = 'Auth User',
            password = 'TestPass123!'
        )

    def test_register(self):
        response = self.client.post('/api/auth/register/', {
            'email':     'new@test.com',
            'name':      'New User',
            'password':  'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_password_mismatch(self):
        response = self.client.post('/api/auth/register/', {
            'email':     'new2@test.com',
            'name':      'New User',
            'password':  'TestPass123!',
            'password2': 'WrongPass123!',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_returns_tokens(self):
        response = self.client.post('/api/auth/login/', {
            'email':    'auth@test.com',
            'password': 'TestPass123!',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_profile_requires_auth(self):
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_returns_user_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'auth@test.com')