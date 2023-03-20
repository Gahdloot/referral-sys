import os
from django.test import TestCase
from django.contrib.auth.password_validation import validate_password
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your tests here.

class SecretKeyTestCase(TestCase):

    def test_secret_key_strength(self):
        SECRET_KEY = os.environ.get('SECRET_KEY')
        try:
            is_strong = validate_password(SECRET_KEY)
        except Exception as e:
            msg = f'Weak Secret Key {e.messages}'
            self.fail(msg)

class LoginTestCase(APITestCase):
    
    def setUp(self):
        self.login_url = reverse('login')
        self.user = User.objects.create_superuser(email='testuser@gmail.com', password='password12345678')
        
    def test_login(self):
        data = {
            "email":"testuser@gmail.com",
            "password":"password12345678"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_user_cannot_login_with_invalid_credentials(self):
        data = {
            'email':'testuser@example.com',
            'password': 'wrong_password'
        }
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, 400 )


class LogoutTestCase(APITestCase):
    
    def setUp(self) -> None:
        self.login_url = reverse('api_logout')
        self.user = User.objects.create_superuser(email='testuser@gmail.com', password='password12345678')

    def test_logout(self):
        data = {
            'email':'testuser@gmail.com',
            'password': 'password12345678'
        }
        # SEND A POST REQUEST TO GET THE TOKEN
        response_login = self.client.post(reverse('login'), data, format='json')
        # STORE TOKEN IN HEADER
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response_login.json().get('token'))

        #test if authenticated user can access a protected endpoint

        # Log out
        response = self.client.post(reverse('api_logout'))
        self.assertEqual(response.status_code, 200)

        # Ensure the user is no longer authenticated and cannot access the protected endpoint







# ========================================================================= #
    # Ensure the user is initially authenticated and can access a protected endpoint
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # response = self.client.get('/protected-endpoint/')
        # self.assertEqual(response.status_code, 200)

        # # Send a POST request to the logout endpoint to log out the user
        # response = self.client.post('/logout/')
        # self.assertEqual(response.status_code, 204)

        # # Ensure the user is no longer authenticated and cannot access the protected endpoint
        # response = self.client.get('/protected-endpoint/')
        # self.assertEqual(response.status_code, 401)