import os
from django.test import TestCase
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from .serializers import UserSerializer
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


class TokenCreationTestCase(APITestCase):
    
    def setUp(self):
        self.login_url = reverse('login')
        self.user = User(email='testuser@gmail.com', is_active=True)
        self.user.set_password('password12345678')
        self.user.save()
        
    def test_token_created_on_login(self):
        data = {
            "email":"testuser@gmail.com",
            "password":"password12345678"
        }
        response = self.client.post(self.login_url, data, format='json')
        # check that the response contains a token
        self.assertIn('token', response.data)
        # check that a token was created for the user
        token = Token.objects.get(user=self.user)
        self.assertIsNotNone(token)


class LoginTestCase(APITestCase):
    
    def setUp(self):
        self.login_url = reverse('login')
        # self.user = User.objects.create_superuser(email='testuser@gmail.com', password='password12345678')
        self.user = User(email='testuser@gmail.com', is_active=True)
        self.user.set_password('password12345678')
        self.user.save()
        
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
        # self.login_url = reverse('api_logout')
        # self.user = User.objects.create_superuser(email='testuser@gmail.com', password='password12345678')
        self.user = User(email='testuser@gmail.com', is_active=True)
        self.user.set_password('password12345678')
        self.user.save()

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


class RegisterTestCase(APITestCase):
    def setUp(self) -> None:
        self.login_url = reverse('login')
        self.register_url = reverse('api_register')
        self.user = User(email='testuser@gmail.com', is_active=True)
        self.user.set_password('password12345678')
        self.user.save()

    def test_register(self):
        # login_data = {
        #     'email':'testuser@gmail.com',
        #     'password': 'password12345678'
        # }
        # response_login = self.client.post(self.login_url, login_data, format='json')
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response_login.json().get('token'))
        
        #Test register view
        register_data = {
            "email":"admin5@gmail.com",
            "first_name": "admin5",
            "last_name": "admin2",
            "phone": "08039550948",
            "company_name": "Great Kart",
            "password":"admin12345678",
            "confirm_password":"admin12345678"
        }
        response = self.client.post(self.register_url, register_data, format='json')
        self.assertEqual(response.status_code, 201)


class UserSerializerTest(TestCase):
    def setUp(self):
        # self.instance = User.objects.create(name="Test Model")
        self.valid_data = {
            "email":"testemail@gmail.com",
            "first_name": "admin5",
            "last_name": "admin2",
            "phone": "08039550948",
            "company_name": "Referral sys",
            "password":"admin12345678",
            "confirm_password":"admin12345678"
        }
        self.invalid_data = {
            "email":"test",
            "first_name": "admin5",
            "last_name": "admin2",
            "phone": "0803955094",
            "company_name": "Referral sys",
            "password":"adm12345678",
            "confirm_password":"admin12345"
        }
        self.user = User(
            email='nwakachibueze@gmail.com',
            first_name='Test',
            last_name='Testing',
            phone='08039550860',
            company_name='Read comps',
        )
        self.user.set_password('admin12345678')
        self.user.save()
        self.serializer = UserSerializer(instance=self.user)

    def test_serializer_fields(self):
        expected_fields = ['email', 'first_name', 'last_name', 'phone', 'company_name']
        self.assertEqual(list(self.serializer.data.keys()), expected_fields)

    def test_serializer_validation(self):
        # Test invalid data
        serializer = UserSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())

        # Test valid data
        serializer = UserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_save(self):
        # Test saving a new instance
        serializer = UserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.email, self.valid_data['email'])

        # Test updating an existing instance
        # serializer = UserSerializer(instance=self.user, data=self.valid_data)
        # self.assertTrue(serializer.is_valid())
        # instance = serializer.save()
        # self.assertEqual(instance.email, self.valid_data['email'])






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