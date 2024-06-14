from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')

def create_user(**prams):
    return get_user_model().objects.create_user(**prams)

class TestPublicUserAPI(TestCase):
    """ API Tests for unauthorized users """

    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_successful(self):
        payload = {
            'email': 'test@email.com',
            'password': 'testpassword123',
            'name': 'test name'
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)
    
    def test_user_already_exists_fail(self):
        payload = {
            'email': 'test@email.com',
            'password': 'testpassword123',
            'name': 'test name'
        }
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)
    
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_password_must_be_8_char_or_more(self):
        payload = {'email':'test@email.com', 'password':'test123'}
        response = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.filter(email=payload['email'])

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user)
    
    def test_create_token_for_user_successfully(self):
        payload = {'email': 'test@email.com', 'password': 'testpassword123'}
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_create_token_for_user_with_invalid_credentials_fail(self):
        create_user(email='test@email.com', password='testpassword123')
        payload = {'email':'test@email.com', 'password':'wrongpassword'}
        response = self.client.post(TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
    
    def test_create_token_fail_if_user_not_exists(self):
        payload = {'email': 'test@email.com', 'password': 'testpassword123'}
        response = self.client.post(TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
    

    def test_create_token_without_password_fail(self):
        payload = {'email': 'test@email.com', 'password': ''}
        response = self.client.post(TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
        

        






