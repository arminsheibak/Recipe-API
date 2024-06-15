from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from recipes.serializers import RecipeSerializer

RECIPE_URL = reverse('recipes:myrecipe-list')

def sample_recipe(user, **params):
    defaults = {
        'title': 'sample_recipe',
        'time_minutes': 10,
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class TestPublicRecipeAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        response = self.client.get(RECIPE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateRecipeAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@email.com', password='password123')
        self.client.force_authenticate(self.user)
    
    def test_retrieve_recipes_successfully(self):
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        response = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_recipes_limited_to_user(self):
        other_user = get_user_model().objects.create_user(email='2@email.com', password='password123')
        sample_recipe(user=self.user)
        sample_recipe(user=other_user)

        response = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)

