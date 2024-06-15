from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe, Tag, Ingredient
from recipes.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse('recipes:myrecipe-list')

def detail_url(recipe_id):
    return reverse('recipes:myrecipe-detail', args=[recipe_id])

def sample_recipe(user, **params):
    defaults = {
        'title': 'sample_recipe',
        'time_minutes': 10,
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)

def sample_tag(user, name='name'):
    return Tag.objects.create(user=user, name=name)

def sample_ingredient(user, name='title'):
    return Ingredient.objects.create(user=user, name=name)

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

    def test_view_recipe_detail(self):
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))
        url = detail_url(recipe.id)

        response = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)