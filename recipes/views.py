from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag
from .serializers import TagSerializer


class TagViewSet(ListModelMixin,CreateModelMixin, GenericViewSet):
    serializer_class = TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(user_id=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)