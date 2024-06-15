from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Ingredient
from recipes.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipes:ingredient-list')

class TestPublicIngredientAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        response = self.client.get(INGREDIENTS_URL)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateIngredientAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@email.com', password='testpassword123')
        self.client.force_authenticate(self.user)
    
    def test_retrieve_ingredients(self):
        Ingredient.objects.create(name='ing 1', user=self.user)
        Ingredient.objects.create(name='ing 2', user=self.user)

        response = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_retrieved_ingredients_belongs_to_authenticated_user(self):
        other_user = get_user_model().objects.create_user(email='2@email.com', password='password1')
        Ingredient.objects.create(name='ing 1', user=self.user)
        Ingredient.objects.create(name='ing 1', user=other_user)

        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'ing 1')

