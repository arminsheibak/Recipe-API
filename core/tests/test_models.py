from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email='test@email.com', password='testpassword123'):
    return get_user_model().objects.create_user(email, password)
class TestModel(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@email.com"
        password = "testpassword123"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'test@EMAIL.COM'
        user = get_user_model().objects.create_user(email=email, password='test123')
        
        self.assertEqual(user.email, email.lower())
    
    def test_new_user_without_email(self):
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(email=None, password='test123')

    def test_create_superuser_successful(self):
        user = get_user_model().objects.create_superuser(email='test@email.com', password='test123')

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_tag_str(self):
        tag = models.Tag.objects.create(user = sample_user(), name='tagname')

        self.assertEqual(str(tag), tag.name)
    
    def test_ingredient_str(self):
        ingredient = models.Ingredient.objects.create(user = sample_user(), name='name')

        self.assertEqual(str(ingredient), ingredient.name)   
    
    def test_recipe_str(self):
        recipe = models.Recipe.objects.create(user= sample_user(), title='recipe', time_minutes=5)

        self.assertEqual(str(recipe), recipe.title)