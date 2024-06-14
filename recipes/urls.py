from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('tags', views.TagViewSet, basename='tag')

app_name = 'recipes'

urlpatterns = [
    path('', include(router.urls))
]