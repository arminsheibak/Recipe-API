from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Tag
from recipes.serializers import TagSerializer

TAGS_URL = reverse('recipes:tag-list')

class TestPublicTagAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        response = self.client.get(TAGS_URL)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateTagAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@email.com', password='testpassword123')
        self.client.force_authenticate(self.user)
    
    def test_retrieve_tags(self):
        Tag.objects.create(name='first tag', user=self.user)
        Tag.objects.create(name='second tag', user=self.user)

        response = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_retrieved_tags_are_for_authenticated_user(self):
        other_user = get_user_model().objects.create_user(email='other@email.com', password='password12')
        Tag.objects.create(name='first tag', user=self.user)
        Tag.objects.create(name='second tag', user=other_user)

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'first tag')


