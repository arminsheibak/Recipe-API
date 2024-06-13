from django.test import TestCase
from django.contrib.auth import get_user_model

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